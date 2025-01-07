// Multiplies the values in R0 and R1 and stores the product in R2.
// R0 and R1 are preset.
// add RAM[0] to RAM[2] and store it in RAM[2], RAM[1] times

// clear RAM[2]
@R2
M=0
// clear RAM[i]
@i
M=0
D=M

(LOOP)
// if i == R1 goto STOP
@R1
D=D-M
@STOP
D;JEQ
// R2 += R0
@R0
D=M
@R2
M=D+M
// i += 1, D=this result
@i
M=M+1
D=M
// goto LOOP
@LOOP
0;JMP






// end state: infinite loop of lines
(STOP)
@STOP
0;JMP