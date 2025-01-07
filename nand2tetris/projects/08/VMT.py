import sys
import os

# file handling, collecting all code lines into one list
files = []
path = os.getcwd() if len(sys.argv) < 2 else sys.argv[1]

if path.endswith('.vm'):  # single file
    files.append(path)
    outputName = os.path.splitext(os.path.basename(path))[0]
elif '.' in path and len(path) > 1:
    exit('VM translator error: Input is not a .vm file or directory, translation terminated.')
else:  # directory
    os.chdir(path)
    for file in os.listdir():
        if file.endswith('.vm'):
            files.append(file)
    outputName = os.path.normpath(path).split('\\')[-1]
if not files:
    exit('VM translator error: Input directory has no .vm files, translation terminated.')

VMcode = []
FILE_SECTIONS = {}
for fileNum, f in enumerate(files):
    with open(f, 'r') as source:
        for line in source:
            line = line.strip()
            if not line.startswith('//') and len(line) > 0:  # ignore comments and blank lines
                VMcode.append(line)
    lineNum = len(VMcode) - 1
    FILE_SECTIONS[lineNum] = f


# commonly used asm code blocks
HALF_POP = '@SP\nAM=M-1\nD=M\n'  # SP -= 1, D = top of stack
GOTO_STACK = '@SP\nA=M-1\n'  # A = SP - 1
PUSH_D = '@SP\nM=M+1\nA=M-1\nM=D\n'  # SP += 1 , append value in D to the stack

# translation dictionaries
BASE_CODES = {'pointer': 3, 'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT', 'temp': 5}
AL_CODES = {'add': '+', 'sub': '-', 'and': '&', 'or': '|'}


# translation functions
def translate_pushpop(isPush, base, offset):
    """Returns a string of multiple lines of assembly code corresponding to a single push/pop VM instruction."""
    if base == 'constant':
        return f"@{offset}\nD=A\n{PUSH_D}"

    if base == 'static':
        gotoAddress = f"@{currFile}.{offset}\n"
    else:
        M_or_A = 'A' if base in ['pointer', 'temp'] else 'M'
        base = BASE_CODES[base]  # encode base to assembly-compatible symbol or number
        gotoAddress = f"@{offset}\nD=A\n@{base}\nA={M_or_A}+D\n"  # A = addr(base) + offset

    if isPush:
        return f"{gotoAddress}D=M\n{PUSH_D}"
    else:
        return f"{gotoAddress}D=A\n@R15\nM=D\n{HALF_POP}@R15\nA=M\nM=D\n"  # address to store in is saved in R15

cmpCount = 0  # TODO neutralize globals

def translate_AL(op):
    """Returns a string of multiple lines of assembly code corresponding to a single arithmetic/logic VM instruction
    Unfortunately, the only way to test for eq, gt, and lt is to use jump instructions."""
    global cmpCount

    if op[0] == 'n':  # single operand: neg, not
        return f"{GOTO_STACK}M={'-' if op == 'neg' else '!'}M\n"

    if op in AL_CODES:  # double operand non-cmp: add, sub, and, or
        return f"{HALF_POP}A=A-1\nM=M{AL_CODES[op]}D\n"  # perform operation M = x (+/-/&/|) y

    # double operand cmp: eq, gt, lt
    saveRetAddr = f"@CMP$ret{cmpCount}\nD=A\n@R15\nM=D\n"  # stores return address in R15
    getResult = f"{HALF_POP}A=A-1\nD=M-D\nM=0\n"  # M = false (0), D = x - y
    jumpLogic = f"@CMP_TRUE\nD;J{op.upper()}\n(CMP$ret{cmpCount})\n"  # jump to code setting M = true (-1) if needed

    cmpCount += 1
    return f"{saveRetAddr}{getResult}{jumpLogic}"

def translate_call(funcName, numFuncArgs):
    """Returns a string of multiple lines of assembly code corresponding to a VM function call.
    Pushes the return address, then the frame, then repositions ARG and LCL, then jumps, leaving behind
    a label to jump back to when the callee finishes executing. ARG = &retAddr when numFuncArgs == 0."""
    retAddr = f"{currFunction}$ret{localCallCount}"

    pushRetAddr = f"@{retAddr}\nD=A\n{PUSH_D}"
    pushLCL = f"@LCL\nD=M\n{PUSH_D}"
    pushARG = f"@ARG\nD=M\n{PUSH_D}"
    pushTHIS = f"@THIS\nD=M\n{PUSH_D}"
    pushTHAT = f"@THAT\nD=M\n{PUSH_D}"
    newARG = f"@{5+int(numFuncArgs)}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n"  # ARG = SP - 5 - numFuncArgs
    newLCL = "@SP\nD=M\n@LCL\nM=D\n"  # LCL = SP (the function pushes zeros that serve as its LCL segment)
    gotoFunc = f"@{funcName}\n0;JMP\n"
    retAddrLbl = f"({retAddr})\n"
    return f"{pushRetAddr}{pushLCL}{pushARG}{pushTHIS}{pushTHAT}{newARG}{newLCL}{gotoFunc}{retAddrLbl}"

def translate_function(funcName, numLocals):
    """Returns a string of multiple lines of assembly code corresponding to a VM function declaration.
    Places a jump point at the start of the function and pushes the necessary amount of zeros for the LCL segment."""
    numLocals = int(numLocals)
    if numLocals > 0:
        pushZeros = f"@{numLocals}\nD=A\n@SP\nM=M+D\nA=M-D\n" + "M=0\nA=A+1\n" * numLocals
        return f"({funcName})\n{pushZeros}"
    return f"({funcName})\n"

def translate_return():
    """Returns a string of multiple lines of assembly code corresponding to a VM function declaration.
    Takes advantage of the fact that LCL is just above the 5 frame elements. Saves the return address,
    puts the return value and SP where they should be, then 'walks' LCL down the frame, restoring the caller's stuff
    in the process."""
    LCL_walkdown = '@LCL\nAM=M-1\nD=M\n'

    saveRetAddr = f"@5\nD=A\n@LCL\nA=M-D\nD=M\n@R14\nM=D\n"  # R14 = *(LCL - 5) == RAM[LCL - 5] = retAddr
    pushReturnValue = f"{HALF_POP}@ARG\nA=M\nM=D\nD=A\n@SP\nM=D+1\n"  # *ARG = pop(), SP = ARG + 1
    reinstateTHAT = f"{LCL_walkdown}@THAT\nM=D\n"
    reinstateTHIS = f"{LCL_walkdown}@THIS\nM=D\n"
    reinstateARG = f"{LCL_walkdown}@ARG\nM=D\n"
    reinstateLCL = f"{LCL_walkdown}@LCL\nM=D\n"
    goBack = f"@R14\nA=M\n0;JMP\n"

    return f"{saveRetAddr}{pushReturnValue}{reinstateTHAT}{reinstateTHIS}{reinstateARG}{reinstateLCL}{goBack}"


# driver code
with open(f'{outputName}.asm', 'w') as output:

    localCallCount = 0  # setting up
    currFile = files[0][:-3]
    currFunction = None

    if '-b' in sys.argv:
        output.write('// This file was generated by the custom VM translator with bootstrapping code.\n')
        output.write('// SP = 256\n')
        output.write('@256\nD=A\n@SP\nM=D\n')  # SP = 256
        output.write('// call Sys.init\n')
        output.write(translate_call("Sys.init", 0))  # call Sys.init
    else:
        output.write('// This file was generated by the custom VM translator without bootstrapping code.\n')
        output.write('// Use \'-b\' in the command line to include booststrapping code.\n')
        output.write('@8\n0;JMP\n')

    output.write('// Top of stack = -1 (used for comparisons)\n')
    output.write(f'(CMP_TRUE)\n{GOTO_STACK}M=-1\n@R15\nA=M\n0;JMP\n')

    instructions = {
        'push': lambda args: translate_pushpop(True, args[1], args[2]),
        'pop': lambda args: translate_pushpop(False, args[1], args[2]),
        'label': lambda args: f"({currFunction + '$'}{args[1]})\n",
        'if-goto': lambda args: f"{HALF_POP}@{currFunction + '$'}{args[1]}\nD;JNE\n",
        'goto': lambda args: f"@{currFunction + '$'}{args[1]}\n0;JMP\n",
        'call': lambda args:  translate_call(args[1], args[2]),
        'function': lambda args: translate_function(args[1], args[2]),
        'return': lambda args: translate_return(),
        'arithmetic-logic-operator': lambda args: translate_AL(args[0])
    }

    for lineNum, line in enumerate(VMcode):
        if lineNum in FILE_SECTIONS:
            currFile = FILE_SECTIONS[lineNum]

        lineParts = line.split()  # split each VM code line into its components: [VMarg0, VMarg1, VMarg2]
        if lineParts[0] == 'function':
            currFunction = lineParts[1]
            localCallCount = 0
        elif lineParts[0] == 'call':
            localCallCount += 1

        translator = instructions.get(lineParts[0], instructions['arithmetic-logic-operator'])
        assembly = translator(lineParts)

        output.write(f'// {line}\n')  # comment
        output.write(assembly)  # asm instructions

    output.write("\n// Ensures infinite loop is present at the end\n")
    output.write("(END_FAILSAFE)\n@END_FAILSAFE\n0;JMP\n")