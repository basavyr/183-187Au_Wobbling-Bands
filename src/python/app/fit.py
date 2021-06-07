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

    @staticmethod
    def Data_Fit_P0(model, x_data_exp, y_data_exp, p_initial):
        """
        Create the fit procedure via curve_fit, using starting values for the fitting parameters."""

        x_data = np.asarray(x_data_exp)
        y_data = np.asarray(y_data_exp)

        params, covariance = curve_fit(
            model, x_data_exp, y_data_exp, p0=p_initial)

        return params, covariance


class Mock_Fit:

    @staticmethod
    def Fit(mock_data, model):

        xdata = np.asarray(mock_data[0])
        ydata = np.asarray(mock_data[1])

        fit_results = Fit.Data_Fit(model, xdata, ydata)

        return fit_results


def Main():
    true_params = [1, 2, 3]

    model = energies.Energy_Formula.Energy1

    xdata = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    true_ydata = [model(
        x, true_params[0], true_params[1], true_params[2]) for x in xdata]

    mock_ydata = [-0.10266646127212908, 7.812282901372733, -3.2278135465579325, 21.443416309796348, 13.103181055729578,
                  38.902538519456996, 42.7913558921784, 41.13754701768447, 53.78640767067495, 91.0827080115583, 101.41853935050891, 114.99844409250798]

    mock_data = [xdata, mock_ydata]
    params = Mock_Fit.Fit(mock_data, model)[0]
    print(params)

    x = Fit.Data_Fit_P0(model, xdata, mock_ydata, [12, 12, 11])
    print(x[0])


if __name__ == '__main__':
    Main()
