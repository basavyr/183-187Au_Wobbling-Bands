import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import energies

p1 = 1
p2 = 2
p3 = 3

x_data = np.arange(0, 10, 0.5)
y_data = [energies.Energy_Formula.Energy1(x, p1, p2, p3) for x in x_data]

xdata = np.asarray(x_data)
ydata = np.asarray(y_data)

params, covariance = curve_fit(energies.Energy_Formula.Energy1, xdata, ydata)

print(params)
