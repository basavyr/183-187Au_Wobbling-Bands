import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import energies

import operator

import plot


class Fit:

    @staticmethod
    def Data_Fit(model, xdata, ydata):

        x_data = np.asarray(xdata)
        y_data = np.asarray(ydata)

        try:
            params, covariance = curve_fit(
                model, x_data, y_data)
        except Exception:
            return None
        else:
            return params, covariance

    @staticmethod
    def Data_Fit_P0(model, xdata, ydata, initial_params):
        """
        Create the fit procedure via curve_fit, using starting values for the fitting parameters."""

        x_data = np.asarray(xdata)
        y_data = np.asarray(ydata)

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

        # print(data)
        return data


# class Mock_Fit:

#     @staticmethod
#     def Generate_Data(model, params):
#         xdata = [int(x) for x in range(-1, 11)]
#         ydata = [model(
#             x, params[0], params[1], params[2]) for x in xdata]

#         data = [xdata, ydata]

#         return data

#     @staticmethod
#     def Fit(mock_data, model):

#         xdata = np.asarray(mock_data[0])
#         ydata = np.asarray(mock_data[1])

#         fit_results = Fit.Data_Fit(model, xdata, ydata)

#         return fit_results

#     @staticmethod
#     def Fit_P0(mock_data, model, initial_params):

#         xdata = np.asarray(mock_data[0])
#         ydata = np.asarray(mock_data[1])

#         fit_results = Fit.Data_Fit_P0(model, xdata, ydata, initial_params)

#         return fit_results

#     @staticmethod
#     def Check_Mock_Data(model, xdata, params):
#         ydata = [model(x, params[0], params[1], params[2]) for x in xdata]
#         return ydata
