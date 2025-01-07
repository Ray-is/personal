import sys
try:
    filePath = sys.argv[1]
except IndexError:
    exit('VM Translator Error: No input file provided')
if filePath[-3:] != ".vm":
    exit('VM Translator Error: Input file is not a .vm file')

VMcode = []
with open(filePath, 'r') as f:
    for line in f:
        line = line.strip()
        if line[0:2] == '//' or len(line) == 0:  # ignore comments and blank lines
            continue
        VMcode.append(line)

pop = '@SP\nAM=M-1\nD=M\n'  # RAM[SP] -= 1, D = top of stack
gotoTop = '@SP\nA=M-1\n'  # A = RAM[SP] - 1
pushD = '@SP\nM=M+1\nA=M-1\nM=D\n'  # RAM[SP] += 1 , append value in D to the stack

base_codes = {'pointer': 3, 'local': 1, 'argument': 2, 'this': 3, 'that': 4, 'temp': 5, 'static': 16}
def translate_pushpop(isPush, base, offset):
    """Returns a string of multiple lines of assembly code corresponding to a single push/pop VM instruction."""
    if base == 'constant':
        return f"@{offset}\nD=A\n{pushD}"

    M_or_A = 'A' if base in ['pointer', 'temp'] else 'M'  # pointer and temp mark the start of their segments,
    base = base_codes[base]  # all others mark the RAM address that holds the location of the start of their segments

    gotoAddress = f"@{offset}\nD=A\n@{base}\nA={M_or_A}+D\n"  # A = addr(base) + offset
    if isPush:
        return f"{gotoAddress}D=M\n{pushD}"
    else:
        return f"{gotoAddress}D=A\n@R15\nM=D\n{pop}@R15\nA=M\nM=D\n"  # address to store in is saved in R15

AL_codes = {'add': '+', 'sub': '-', 'and': '&', 'or': '|'}
cmpCount = 0
def translate_AL(op):
    """Returns a string of multiple lines of assembly code corresponding to a single arithmetic/logic VM instruction"""
    global cmpCount

    if op[0] == 'n':  # single operand: neg, not
        return f"{gotoTop}M={'-' if op == 'neg' else '!'}M\n"

    if op in AL_codes:  # double operand non-cmp: add, sub, and, or
        return f"{pop}A=A-1\nM=M{AL_codes[op]}D\n"  # perform operation M = x (+/-/&/|) y

    # double operand cmp: eq, gt, lt
    saveLocation = f"@RETADDR_CMP{cmpCount}\nD=A\n@R15\nM=D\n"  # stores line number to return to in R15
    getResult = f"{pop}A=A-1\nD=M-D\nM=0\n"  # M = 0, D = x - y
    jumpLogic = f"@CMP_TRUE\nD;J{op.upper()}\n(RETADDR_CMP{cmpCount})\n"  # jump to code setting M = -1 if needed

    cmpCount += 1
    return f"{saveLocation}{getResult}{jumpLogic}"

def translate_label(lbl):
    return f"({lbl})\n"

def translate_ifgoto(lbl):
    return f"{gotoTop}D=M\n@{lbl}\nD;JLT\n"

def translate_goto(lbl):
    return f"@{lbl}\n0;JMP\n"

# driver code
with open(f'{filePath[:-3]}.asm', 'w') as output:
    output.write('// Initialization (this file was generated by the VM translator)\n')
    output.write('@256\nD=A\n@SP\nM=D\n')  # SP set to 256
    output.write('@START\n0;JMP\n\n')  # bypass next section
    output.write(f'(CMP_TRUE)\n{gotoTop}M=-1\n@R15\nA=M\n0;JMP\n\n')  # top of stack = -1 (used for comparisons)
    output.write('(START)\n')

    for line in VMcode:
        lineParts = line.split()
        if len(lineParts) == 1:
            assembly = translate_AL(line)
        elif lineParts[0] == 'push':
            assembly = translate_pushpop(True, lineParts[1], lineParts[2])
        elif lineParts[0] == 'pop':
            assembly = translate_pushpop(False, lineParts[1], lineParts[2])
        elif lineParts[0] == 'label':
            assembly = translate_label(lineParts[1])
        elif 'if' in lineParts[0]:
            assembly = translate_ifgoto(lineParts[1])

        output.write(f'// {line}\n')  # comment
        output.write(assembly)  # instruction(s)

    output.write('// infinite loop end\n')
    output.write('(END)\n@END\n0;JMP\n')

# verbose printing
if '-v' in sys.argv:
    for line in VMcode:
        print(line)