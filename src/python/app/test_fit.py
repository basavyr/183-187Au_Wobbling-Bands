import numpy as np
from scipy.optimize import curve_fit


def func3(X, p1, p2, p3):
    x1, x2, x3 = X
    return p1 * x1 + p2 * x2 + p3 * x3


# some artificially noisy data to fit
x1 = [i for i in range(0, 100)]
x2 = [i for i in range(0, 100)]
x3 = [i for i in range(0, 100)]
W = [i for i in range(0, 100)]

a, b, c = 10., 4., 6.

X = (x1, x2, x3)

p0 = 8., 2., 7.

print(curve_fit(func3, X, W, p0))
