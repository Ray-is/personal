import warnings
from sys import path
path.insert(0,r"C:\Users\Raymond\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages")
from PIL import Image
import numpy as np
warnings.filterwarnings('ignore')

W, H = 1500,1500
setCenter = -0.5 - 0j
xScale = 1.3
yScale = 1.3
maxIterations = int(input('Iteration count: '))

re = np.linspace(-xScale + setCenter.real, xScale + setCenter.real, W)
im = np.linspace((-yScale + setCenter.imag), (yScale + setCenter.imag), H)
cplxNums = re[np.newaxis, :] + im[:, np.newaxis] * 1j #Generate a corresponding complex number for each pixel

def mainFunc(c):
    z = 0
    escapeTime = 0
    for _ in range(maxIterations):
        escapeTime += 1
        z = z ** 2 + c #Formula to iterate
        if abs(z) > 100:
            return escapeTime
    return 0

def fastFunc(c):
    z = 0
    for _ in range(maxIterations):
        z = z ** 2 + c
    return abs(z) < 3

mainFunc = np.vectorize(mainFunc)
pixels = np.array(mainFunc(cplxNums)) #Call mainFunc on each complex number and store results in array
print('Mapping findings to image')

result = Image.new('L', (W, H))
for Y in range(H):
    for X in range(W):
        if int(pixels[Y, X]) == 0:
            result.putpixel((X, Y), 0)
        else:
            result.putpixel((X, Y), int(pixels[Y,X]) * 5)

result.show()