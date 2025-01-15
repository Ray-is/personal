from sys import path
path.insert(0,'sympy'); path.insert(0, 'mpmath')
import sympy as sp

accuracy = 1e-9

print('\nNewton\'s method root finder\nUse \"p\" for pi.')
print(30*'-')
f = sp.parse_expr(input('f(x) = ').replace('^','**'), transformations='implicit') #Get input and process it into f(x)
f = f.subs('e', sp.exp(1)); f = f.subs('p', sp.pi); x = sp.symbols('x') #Define x and constants
fPrime = sp.diff(f) #Get derivative

guess = sp.parse_expr(input('Enter a guess: ')).evalf()
n = -1
def newtonMethod(x0, prev):
    global n; n += 1 #Increment iteration counter

    denom = fPrime.subs(x, x0).evalf()
    try:
        if denom >= 1e31: #End condition: f'(x0) is too large or imaginary
            print(f'f\'(x{n}) is too large. Could not find a root.'); return
    except TypeError:
        print(f'f\'(x{n}) is undefined. Could not find a root.'); return
    if 1e-16 >= denom >= 0: #End condition: f'(x0) is extremely close to zero
        print(f'f\'(x{n}) is too close to zero. Could not find a root.'); return

    print(f'x{n}: {x0}')
    if abs(prev - x0) < accuracy: #End condition: difference of two consecutive iterations is sufficiently small
        print(f'Found approximate root after {n} iterations: {x0:.8f}'); return

    nextGuess = (x0 - f.subs(x, x0) / denom).evalf() #Newton's method formula: x0 - f(x0) / f'(x0)
    newtonMethod(nextGuess, x0) #Keep iterating if end conditions are not met

try:
    newtonMethod(guess, 0)
except RecursionError:
    print(f'Could not approximate a root to 8 decimal places after {n} iterations.')