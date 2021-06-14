import numpy as np
from scipy.optimize import curve_fit
import warnings


def func(X, a, b, c):
    DEBUG_MODE = False
    x, y = X
    if(DEBUG_MODE):
        print(f'x-> {x}')
        print(f'y-> {y}')
    with np.errstate(divide="ignore"):
        result = a * x + b * y + c
    if(DEBUG_MODE):
        print(f'ravel-> {result.ravel()}')
    return result.ravel()


y = np.arange(1, 5, 1)
x = np.arange(1, 5, 1)

mesh = np.meshgrid(x, y)
a, b, c = 10., 4., 6.

with open('x.dat', 'w+') as writer:
    for x in mesh:
        writer.write(str(x))
        writer.write('\n')
    writer.write(str(len(mesh[0])))
    writer.write('\n')
    writer.write(str(mesh[0][0]))
    writer.write('\n')
    writer.write(str(mesh[1][0]))
    writer.write('\n')
    writer.write(str(mesh[1][1]))


z = func(mesh, a, b, c) + np.random.random(len(x) * len(y))
# print(z)
p0 = 1., 1., 1.
print(curve_fit(func, mesh, z, p0))
