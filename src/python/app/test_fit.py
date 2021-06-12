import numpy as np
from scipy.optimize import curve_fit
import warnings


def func(X, a, b, c):
    x, y = X
    print(f'x-> {x}')
    print(f'y-> {y}')
    with np.errstate(divide="ignore"):
        result = x + y
    print(f'ravel-> {result.ravel()}')
    return result.ravel()


y = np.arange(0, 5, 1)
x = np.arange(0, 5, 1)
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

func(mesh, a, b, c)
# z = func(X, a, b, c) * 1 + np.random.random(xdim * ydim) / 100

# p0 = 8., 2., 7.
# print(curve_fit(func, X, z, p0))
