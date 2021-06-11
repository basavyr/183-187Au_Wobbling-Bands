import sys
from numpy import sqrt
import energies
import fit
import plot


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
    return 1


def Energy_Function_Arrays():

    spins = energies.np.arange(4.5, 28.8, 2)
    wobbling_phonons = [0 if x % 2 == 0 else 1 for x in range(len(spins))]

    # evaluation of the excitation energy for all the spins and wobbling phonon numbers of the band
    # this is a 1-D array that results from applying E_exc on the entire set of spins and wobbling phonons
    f_xy_data = energies.Models.Model_Energy_i13_2(
        (spins,spins), 60, 20, 4, 4, 20)

    # fit_results = fit.curve_fit(
    #     energies.Models.Model_Energy_i13_2, (spins, wobbling_phonons), f_xy_data)
    # print(fit_results)


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
