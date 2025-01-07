import sys
try:
    filePath = sys.argv[1]
except IndexError:
    exit('Hack Assembler Error: No input file provided')
if filePath[-4:] != ".asm":
    exit('Hack Assembler Error: Input file is not a .asm file')

symbolCode = []
with open(filePath, 'r') as f:
    for line in f:
        line = ''.join(line.split())  # remove all whitespace
        if line[0:2] == '//' or len(line) == 0:  # ignore comments and blank lines
            continue
        symbolCode.append(line)

ac6_codes = {'0': '0101010',  # lookup table for the acccccc or "comp" part of a c instruction
             '1': '0111111',
             'D': '0001100',
             'A': '0110000',
             'M': '1110000',
             '-1': '0111010',
             '!D': '0001101',
             '!A': '0110001',
             '!M': '1110001',
             '-D': '0001111',
             '-A': '0110011',
             '-M': '1110011',
             'D+1': '0011111',
             'A+1': '0110111',
             'M+1': '1110111',
             'D-1': '0001110',
             'A-1': '0110010',
             'M-1': '1110010',
             'D+A': '0000010',
             'A+D': '0000010',
             'D+M': '1000010',
             'M+D': '1000010',
             'D-A': '0010011',
             'D-M': '1010011',
             'A-D': '0000111',
             'M-D': '1000111',
             'D&A': '0000000',
             'A&D': '0000000',
             'D&M': '1000000',
             'M&D': '1000000',
             'D|A': '0010101',
             'A|D': '0010101',
             'D|M': '1010101',
             'M|D': '1010101'}

j3_codes = {None: '000',  # lookup table for the jjj or "jmp" part of a C-instruction
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'}

def assemble_C_instruction(C_inst):
    """Transforms an assembly C instruction to a hack machine language C instruction of the format 111accccccdddjjj"""

    # Separate instruction into dest, comp, and jmp segments
    if '=' in C_inst:
        dest, comp_jmp = C_inst.split('=')
        try:
            comp, jmp = comp_jmp.split(';')
        except ValueError:
            comp, jmp = comp_jmp, None
    else:
        dest = None
        try:
            comp, jmp = C_inst.split(';')
        except ValueError:
            comp, jmp = C_inst, None

    # Transform segments into binary and concatenate them
    prefixed_ac6 = '111' + ac6_codes[comp]  # 111acccccc
    destinations = ['0', '0', '0']  # ddd
    try:
        if 'A' in dest:
            destinations[0] = '1'
        if 'D' in dest:
            destinations[1] = '1'
        if 'M' in dest:
            destinations[2] = '1'
    except TypeError:
        pass
    d3 = ''.join(destinations)
    j3 = j3_codes[jmp]  # jjj
    return prefixed_ac6 + d3 + j3

symbols = {f'@R{i}': i for i in range(16)}
symbols.update({'@SCREEN': 16384,
                '@KBD': 24576,
                '@SP': 0,
                '@LCL': 1,
                '@ARG': 2,
                '@THIS': 3,
                '@THAT': 4})

# first pass, defining symbols for pseudo-instructions
assemblyCode = []
for line in symbolCode:
    if line[0] == '(':  # psuedo-instruction
        symbols['@' + line[1:-1]] = len(assemblyCode)
    else:
        assemblyCode.append(line)

# second pass, defining/referencing symbols and translating assembly to machine code
symbolAddr = 16
with open(f'{filePath[:-4]}.hack', 'w') as output:
    for line in assemblyCode:

        if line[0] == '@' and line[1].isdigit():  # A instruction
            int15 = f'{int(line[1:]):015b}'
            instruction = f'0{int15}'

        elif line[0] == '@':  # Symbolic A instruction
            try:
                decimalNum = symbols[line]
            except KeyError:
                symbols[line] = symbolAddr
                symbolAddr += 1
                decimalNum = symbols[line]
            instruction = f'0{decimalNum:015b}'

        else:  # C instruction
            instruction = assemble_C_instruction(line)

        output.write(instruction + '\n')


if '-v' in sys.argv:
    for s, v in symbols.items():
        print(s, v)