import sys
from numpy import sqrt
import energies
import fit
import plot


def Get_Experimental_Data(isotope):
    """Read the experimental data for a particular band sequence of an isotope.
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

    return [X_DATA_SPINS, X_DATA_PHONONS, Y_DATA]


def Fit_Model(x_data_1, x_data_2, y_data):

    DEBUG_MODE = False

    spins = energies.np.asarray(x_data_1)
    wobbling_phonons = energies.np.asarray(x_data_2)
    if(DEBUG_MODE):
        print(spins)
        print(wobbling_phonons)

    # evaluation of the excitation energy for all the spins and wobbling phonon numbers of the band
    # this is a 1-D array that results from applying E_exc on the entire set of spins and wobbling phonons
    exp_data = energies.np.asarray(y_data)

    if(DEBUG_MODE):
        print(f'Band Head -> {exp_data[0]}')

    band_head = exp_data[0]

    # normalize the experimental data to the band-head
    exp_data_normed = [x - band_head for x in exp_data]

    if(DEBUG_MODE):
        print(exp_data)

    fit_results = fit.curve_fit(
        energies.Models.Model_Energy_i13_2, (spins, wobbling_phonons), exp_data_normed, p0=[80.0, 3.0, 25.0, 1.9, 20.0], bounds=([1, 1, 1, 0.1, 19.0], [100, 100, 100, 9.0, 25.0]))

    if(DEBUG_MODE):
        print(fit_results)

    params = fit_results[0]
    params = [round(p, 3) for p in params]

    # parameter set from Mathematica
    # params_math = [83.4294, 3.64419, 25.7625, 1.99236, 19]
    print(f'Params -> {params}')

    th_data = energies.Models.Model_Energy_i13_2(
        (spins, wobbling_phonons), params[0], params[1], params[2], params[3], params[4])
    if(DEBUG_MODE):
        print(f'Data-> {th_data}')

    print(f'RMS -> {fit.Fit.RMS(exp_data_normed, th_data)}')

    # plot the obtained data
    plot.Plot_Maker.Create_Fit_Plot(
        [spins, exp_data_normed], [spins, th_data], energies.Files.AU_183_POSITIVE_ENERGY_PLOT, 'Positive-Parity')


def Main_183():

    model = energies.Energy_Formula.Excitation_Energy

    plot_location = energies.Files.plot_directory

    def plot_name(label): return f'{plot_location}fit_results_{label}.pdf'

    # Experimental data for $^{183}$Au
    AU_183_POSITIVE = energies.Files.AU_183_DATA_POSITIVE
    AU_183_NEGATIVE = energies.Files.AU_183_DATA_NEGATIVE

    # get the experimental data for the positive parity wobbling bands
    x_data_1, x_data_2, y_data = Get_Experimental_Data(AU_183_POSITIVE)
    # fit the theoretical model to the experimental data extracted at the previous step for the isotope
    Fit_Model(x_data_1, x_data_2, y_data)


if __name__ == '__main__':
    Main_183()
