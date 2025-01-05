from sys import path
path.insert(0,r'C:\Users\Raymond\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages')
import taichi as ti
from taichi import math as tm
from time import sleep
ti.init(arch=ti.gpu, default_fp=ti.f64)

##################### CONTROLS #################
# Left click:  Zoom in on the click
# Right click: Zoom out
# Space:       Double max iterations (resolution)
# Shift:       Half max iterations
# Up arrow:    Increase exponent parameter of iterated formula
# Down arrow:  Decrease exponent
# Capslock:    Swap sign of exponent
# Tab:         Decrease infinity threshold
# 

# Initialize GUI and its pixel data
W, H = 1708, 960
window = ti.GUI(res=(W, H), fast_gui=True, fullscreen=True)
pixelPositions = ti.field(dtype=ti.i8, shape=(W, H))
pixelData = ti.Vector.field(3, dtype=ti.f64, shape=(W,H))

# Initialize parameters and complex vector type
cplxVec = ti.types.vector(2, ti.f64)
setCenter = cplxVec(-0.3, 0)

# these set the aspect ratio
reScale = 2
imScale = 1.3


maxIterations = 256
infinityThreshold = 3
expnt = 2

@ti.kernel
def new_image(reS:ti.f64, imS:ti.f64, cent:cplxVec, maxIter:int, powNum:ti.f64, infinityThreshold: ti.f64):
    for X, Y in pixelPositions: #For each position (0,0) to (W, H):
        c = cplxVec((2 * reS * X) / W - reS + cent[0], (2 * imS * Y) / H - imS + cent[1]) # Convert it to a c value
        z = cplxVec(0,0) # Initial z value
        iterCount = 0
        while iterCount < maxIter and z.norm() < infinityThreshold:
            z = tm.cpow(z, powNum) + c # Formula to iterate
            iterCount += 1

        if iterCount == maxIter: # Color of set members
            pixelData[X, Y] = tm.vec3(0, 0, 0)

        else: # Gradient control of nonmembers
            pixelData[X, Y] = tm.vec3(abs(tm.sin(iterCount / 51)), #R
                                      abs(tm.sin(iterCount / 52)), #G
                                      abs(tm.sin(iterCount / 53))) #B

new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData) # Initial image

while window.running: # Main loop
    window.show(); window.get_event()

    if window.is_pressed(ti.GUI.LMB): # Zoom in on position of the click
        xPos, yPos = window.get_cursor_pos()
        reScale, imScale = reScale / 2, imScale / 2
        setCenter = cplxVec((2 * xPos - 1) * reScale + setCenter[0], (2 * yPos - 1) * imScale + setCenter[1])
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print(f'Zoomed in to {setCenter}, scale = {reScale}')
        sleep(0.3)

    elif window.is_pressed(ti.GUI.RMB): # Zoom out
        reScale, imScale = reScale * 2, imScale * 2
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print('Zoomed out, scale =', reScale)
        sleep(0.3)

    elif window.is_pressed(ti.GUI.SPACE): # Increase max iterations
        maxIterations *= 2
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print('Max Iterations:', maxIterations)
        sleep(0.3)

    elif window.is_pressed(ti.GUI.SHIFT): # Decrease max iterations
        maxIterations //= 2
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print('Iterations:', maxIterations)
        sleep(0.3)

    elif window.is_pressed(ti.GUI.UP): # increase exponent
        expnt += 0.1
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print(f'Pow: {expnt:.2f}')
        sleep(0.3)

    elif window.is_pressed(ti.GUI.DOWN): # decrease exponent
        expnt -= 0.1
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print(f'Pow: {expnt:.2f}')
        sleep(0.3)

    elif window.is_pressed(ti.GUI.CAPSLOCK): # swap sign of exponent
        expnt *= -1
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print(f'Pow: {expnt:.2f}')
        sleep(0.3)

    elif window.is_pressed(ti.GUI.RIGHT): # double infinity threshold
        infinityThreshold *= 2
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print(f'Infinity threshold: {infinityThreshold}')
        sleep(0.3)

    elif window.is_pressed(ti.GUI.LEFT): # half infinity threshold
        infinityThreshold /= 2
        new_image(reScale, imScale, setCenter, maxIterations, expnt, infinityThreshold); window.set_image(pixelData); window.show()
        print(f'Infinity threshold: {infinityThreshold}')
        sleep(0.3)
