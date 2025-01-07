// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// screen: each row is 32 16-bit addresses, 256 rows starting at 16384
// screen range: addresses 16384 (SCREEN) to 24575

(LISTEN)
// if KBD == 0 goto LISTEN
@KBD
D=M
@LISTEN
D;JEQ


// pos = 0
@pos
M=0

(BLACKEN)
// A = 16384 + pos[m]
@SCREEN
D=A
@pos
A=D+M
// M (pixel value) = -1 (black)
M=-1
// pos += 1
@pos
M=M+1
// D = pos - 8192
D=M
@8192
D=D-A
// goto BLACKEN if D != 0
@BLACKEN
D;JNE

// reset pos (pos = 0)
@pos
M=0


(HOLD)
@KBD
D=M
// goto HOLD if KDB != 0
@HOLD
D;JNE


(WHITEN)
// A = 16384 + pos[m]
@SCREEN
D=A
@pos
A=D+M
// M (pixel value) = 0 (white)
M=0
// pos += 1
@pos
M=M+1
// D = pos - 8192
D=M
@8192
D=D-A
// goto WHITEN if D != 0
@WHITEN
D;JNE

// goto LISTEN
@LISTEN
0;JMP