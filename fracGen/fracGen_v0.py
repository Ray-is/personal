import tkinter as tk

W, H = 1000,1000
centerX = W // 2
centerY = H // 2

window = tk.Tk()
graph = tk.Canvas(window, width=W, height=H, bg='#5651d6')
graph.pack()

MS = tk.PhotoImage(width=W, height=H)
graph.create_image(W // 2, H // 2, image=MS, state='normal')

xScale = 2
yScale = 1.2
plotFocus = -0.3 + 0j
showAxes = False
if showAxes:
    graph.create_line((0, centerY), (W, centerY), fill='blue') #x axis
    graph.create_line((centerX, 0), (centerX, H), fill='blue') #y axis
#------------------------------------------------------
def convert_pos_to_num(X,Y):
    re = (X - centerX) * xScale / centerX
    im = (Y - centerY) * yScale / centerY
    return complex(re + plotFocus.real, im - plotFocus.imag)

maxIterations = int(input('Maximum number of iterations: '))

for row in range(H):
    for col in range(W):
        c = convert_pos_to_num(col,row)

        val = 0
        for _ in range(maxIterations):
            val = val ** 2 + c #Formula to iterate
            if abs(val) > 100:
                break
        if abs(val) < 100:
            MS.put('black', (col,row))

    print(f'{row} / {H}')

window.mainloop()