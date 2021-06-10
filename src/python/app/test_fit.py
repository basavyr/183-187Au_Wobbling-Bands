import numpy as np
from scipy.optimize import curve_fit


def func(X, a, b, c):
    x, y = X
    x = np.array(x)
    y = np.array(y)
    return np.log(a) + b * np.log(x) + c * np.log(y)


# some artificially noisy data to fit
x = np.linspace(0.1, 1.1, 100)
y = np.linspace(1., 2., 100)
print(x)
print(y)
a, b, c = 10., 4., 6.
z = func((x, y), a, b, c) + np.random.random(100) / 100
print(z)

# initial guesses for a,b,c:
p0 = 8., 2., 7.
print(curve_fit(func, (x, y), z, p0))
