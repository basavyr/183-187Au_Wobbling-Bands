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


class Mock_Fit:
    mock_xdata = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    mock_ydata = [-0.10266646127212908, 7.812282901372733, -3.2278135465579325, 21.443416309796348, 13.103181055729578,
                  38.902538519456996, 42.7913558921784, 41.13754701768447, 53.78640767067495, 91.0827080115583, 101.41853935050891, 114.99844409250798]

    @staticmethod
    def Fit(mock_ydata):
        return 1


def Main():
    mock_ydata = Mock_Fit.mock_ydata
    params = Mock_Fit.Fit(mock_ydata)


if __name__ == '__main__':
    Main()
