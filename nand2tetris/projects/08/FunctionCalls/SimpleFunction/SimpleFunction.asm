// This file was generated by the custom VM translator without bootstrapping code.
// Use '-b' in the command line to include booststrapping code.
@8
0;JMP
// Top of stack = -1 (used for comparisons)
(CMP_TRUE)
@SP
A=M-1
M=-1
@R15
A=M
0;JMP
// function SimpleFunction.test 2
(SimpleFunction.test)
@2
D=A
@SP
M=M+D
A=M-D
M=0
A=A+1
M=0
A=A+1
// push local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
M=M+1
A=M-1
M=D
// push local 1
@1
D=A
@LCL
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
// not
@SP
A=M-1
M=!M
// push argument 0
@0
D=A
@ARG
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
// push argument 1
@1
D=A
@ARG
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
// return
-1
-1
-1
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A
@SP
M=D+1
@LCL
AM=M-1
D=M
@THAT
M=D
@LCL
AM=M-1
D=M
@THIS
M=D
@LCL
AM=M-1
D=M
@ARG
M=D
@LCL
M=M-1
AM=M-1
D=M
@R14
M=D
@LCL
AM=M+1
D=M
@LCL
M=D
@R14
A=M
0;JMP

// In case ending infinite loop wasn't written in
(END_FAILSAFE)
@END_FAILSAFE
0;JMP
