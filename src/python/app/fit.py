import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import energies

import plot


class Fit:

    @staticmethod
    def Data_Fit(model, x_data_exp, y_data_exp):

        x_data = np.asarray(x_data_exp)
        y_data = np.asarray(y_data_exp)

        params, covariance = curve_fit(
            model, x_data, y_data)

        return params, covariance
