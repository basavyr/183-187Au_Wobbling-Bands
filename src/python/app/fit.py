import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import energies

import operator

import plot


class Fit:

    @staticmethod
    def Data_Fit(model, xdata, ydata):

        DEBUG_MODE = True

        x1, x2 = xdata
        y_data = ydata

        if(DEBUG_MODE):
            print('In fitting procedure\n')
            print(x1)
            print(x2)
            print(y_data)

        try:
            params, covariance = curve_fit(model, xdata=(x1, x2), ydata=y_data)
        except Exception as err:
            print(f'Error while trying to fit the data -> {err}')
            return None
        else:
            return params, covariance

    @staticmethod
    def Data_Fit_P0(model, xdata, ydata, initial_params):
        """
        Create the fit procedure via curve_fit, using starting values for the fitting parameters."""

        try:
            params, covariance = curve_fit(
                model, xdata, ydata, p0=initial_params)
        except Exception:
            return None
        else:
            return params, covariance

    @staticmethod
    def Concatenate_Data(band1, band2):
        data = [b for b in band1]
        for b in band2:
            data.append(b)

        data.sort(key=operator.itemgetter(0))

        return data

    @staticmethod
    def RMS(exp_data, th_data):

        DEBUG_MODE = False

        try:
            assert len(exp_data) == len(th_data)
        except AssertionError:
            return np.inf
        else:
            diffs = [np.power(abs(exp_data[idx] - th_data[idx]), 2)
                     for idx in range(len(exp_data))]
            rms = sum(diffs) / (len(exp_data) + 1)

            if(DEBUG_MODE):
                print(diffs)
                print(rms)
                print(np.sqrt(rms))
                print(len(exp_data))

            return np.sqrt(rms)
