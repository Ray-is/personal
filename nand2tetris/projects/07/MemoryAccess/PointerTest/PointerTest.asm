// Initialization (this file was generated by the VM translator)
@256
D=A
@SP
M=D
@PROGRAM_START
0;JMP

(COMPARE_TRUE)
@SP
A=M-1
M=-1
@R15
A=M
0;JMP

(PROGRAM_START)
// push constant 3030
@3030
D=A
@SP
M=M+1
A=M-1
M=D
// pop pointer 0
@0
D=A
@3
A=A+D
D=A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
// push constant 3040
@3040
D=A
@SP
M=M+1
A=M-1
M=D
// pop pointer 1
@1
D=A
@3
A=A+D
D=A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
// push constant 32
@32
D=A
@SP
M=M+1
A=M-1
M=D
// pop this 2
@2
D=A
@3
A=M+D
D=A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
// push constant 46
@46
D=A
@SP
M=M+1
A=M-1
M=D
// pop that 6
@6
D=A
@4
A=M+D
D=A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
// push pointer 0
@0
D=A
@3
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
// push pointer 1
@1
D=A
@3
A=A+D
D=M
@SP
M=M+1
A=M-1
M=D
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push this 2
@2
D=A
@3
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// push that 6
@6
D=A
@4
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// infinite loop end
(END)
@END
0;JMP
