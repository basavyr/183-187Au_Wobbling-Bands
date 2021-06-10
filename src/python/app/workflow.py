import sys
from numpy import sqrt
import energies
import fit
import plot


class Isotope:

    @staticmethod
    def Fit_Isotope(data):

        try:
            nlm = fit.Mock_Fit.Fit(data, energies.Energy_Formula.Energy1)
        except Exception:
            nlm = -1
            return nlm
        else:
            return nlm


def Main():

    model = energies.Energy_Formula.Energy1

    plot_location = energies.Files.plot_directory

    def plot_name(idx): return f'{plot_location}fit_results_{idx}.pdf'

    idx = 1

    for isotope in energies.Files.EXP_DATA_FILES:
        isotope_data = energies.Extract_Data.Get_Energies(isotope)

        plot_label = isotope_data[2]

        # print(f'Nucleus -> {plot_label}')

        # first band
        band_0 = isotope_data[0]

        # print(band_0)

        # generate x_data
        band_0_spins = [x[0] for x in band_0]
        # generate y_data
        band_0_energies = [x[1] for x in band_0]

        # second band
        # first band
        band_1 = isotope_data[1]
        # generate x_data
        band_1_spins = [x[0] for x in band_1]
        # generate y_data
        band_1_energies = [x[1] for x in band_1]

        data_0 = [band_0_spins, band_0_energies]
        data_1 = [band_1_spins, band_1_energies]

        # print(data_0)
        # print(data_1)

        nlm_0 = Isotope.Fit_Isotope(data_0)
        # nlm_1 = Isotope.Fit_Isotope(data_1)

        print(nlm_0[0])

        exp_data = [band_0_spins, band_0_energies]
        # TODO change with proper theoretical data
        th_data = [band_0_spins, band_0_energies]

        plot.Plot_Maker.Create_Fit_Plot(
            exp_data, th_data, plot_name(idx), plot_label)

        idx += 1
        # print(band_1_energies)
        # print(fit.Mock_Fit.Check_Mock_Data(model, band_1_spins, nlm_1[0]))


def Get_Experimental_Data(isotope):
    """Read the experimental data for a particular band sequence of an isotope
    The data corresponds to the wobbling excitations of an isotope with a defined parity. Namely, there can be band sequences that correspond to positive parity and sequences which correspond to negative parity.

    """

    DEBUG_MODE = False

    YRAST, TW1, LABEL = energies.Extract_Data.Get_Energies(isotope)
    YRAST = energies.Energy_Formula.MeV(YRAST)
    TW1 = energies.Energy_Formula.MeV(TW1)

    EXP_DATA = fit.Fit.Concatenate_Data(YRAST, TW1)

    if(DEBUG_MODE):
        print(f'****** {LABEL} ******')
        print(f'****** Yrast band ******\n{YRAST}')
        print(f'****** TW1 band ******\n{TW1}')
        print(f'****** EXP DATA: ******\n{EXP_DATA}\n')

    X_DATA_SPINS = [X[0] for X in EXP_DATA]
    X_DATA_PHONONS = [X[1] for X in EXP_DATA]
    Y_DATA = [X[2] for X in EXP_DATA]

    if(DEBUG_MODE):
        print([X_DATA_SPINS], [X_DATA_PHONONS])
        print(Y_DATA)

    # return [[X_DATA_SPINS, X_DATA_PHONONS], Y_DATA]
    return [energies.np.meshgrid(X_DATA_SPINS, X_DATA_PHONONS), Y_DATA]


def Fit_Model_Data(isotope):
    # unpack the experimental data for the isotope

    # some artificially noisy data to fit
    x = energies.np.linspace(0.1, 1.1, 101)
    y = energies.np.linspace(1., 2., 101)
    a, b, c = 10., 4., 6.

    z = energies.Models.Model_Energy_i13_2((x, y), 1, 1, 1, 1, 1)
    # z = 1 + energies.np.random.random(101) / 100
    # print(x)
    # print(y)
    # print(z)
    # print(x_data)
    # print(y_data)

    # spins, phonons = x_data

    # print(spins)
    # print(phonons)
    # print(y_data)
    # try:
    #     x_data, y_data = Get_Experimental_Data(isotope)
    # except Exception:
    #     print('Failed getting the experimental data')
    # else:
    #     print(f'{x_data}\n{y_data}')

    # params = fit.Fit.Data_Fit(
    #     energies.Models.Model_Energy_i13_2, X, Y)[0]

    # print(f'Fit results-> {params}')

    # y_data_th = [energies.Models.Model_Energy_i13_2(
    #     x, params[0], params[1], params[2], params[3], params[4]) for x in x_data]

    # print(y_data_th)
    # return params


def Omega_Tests():
    w1 = energies.Energy_Formula.Omega_Frequencies(
        21.5, 6.5, 60, 100, 40, 3, 23)
    w2 = energies.Energy_Formula.Omega_Frequencies(21.5, 6.5, 1, 2, 40, 3, 23)
    w3 = energies.Energy_Formula.Omega_Frequencies(
        21.5, 6.5, 60, 80, 40, 3, 23)
    ww = [bool(x) for x in [w1, w2, w3]]
    print(ww)


def Energy_Function_Arrays():
    spins = energies.np.linspace(0.1, 1.1, 101)
    wobbling_phonons = energies.np.linspace(1., 2., 101)
    # print(x)
    # print(y)
    t1 = energies.Energy_Formula.H_Min(spins, 1, 1, 1, 1, 1, 1)

    t2 = energies.Energy_Formula.Omega_Frequencies(spins, 1, 1, 1, 1, 1, 1)

    t3 = energies.Energy_Formula.Energy_Expression(
        wobbling_phonons, 0, spins, 1, 1, 1, 1, 1, 1)
    t4 = energies.Energy_Formula.Excitation_Energy(
        wobbling_phonons, 0, spins, 1, 1, 1, 1, 1, 1, 1)
    # print(t1)
    # print(t2)
    # print(t3)
    print(len(t4))
    # print(t4)


if __name__ == '__main__':
    AU_183_POSITIVE = energies.Files.AU_183_DATA_POSITIVE
    AU_183_NEGATIVE = energies.Files.AU_183_DATA_NEGATIVE

    # get the experimental data for the positive parity wobbling bands
    # Get_Experimental_Data(AU_183_POSITIVE)

    # Fit_Model_Data(AU_183_POSITIVE)
    Energy_Function_Arrays()
    # print(PARAMS)
    # Fit_Model_Data(AU_183_NEGATIVE)
    # Get_Experimental_Data(AU_183_NEGATIVE)
