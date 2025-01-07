// SP initialization
@256
D=A
@SP
M=D
// push constant 7
@7
D=A
@SP
AM=M+1
A=A-1
M=D
// push constant 8
@8
D=A
@SP
AM=M+1
A=A-1
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
