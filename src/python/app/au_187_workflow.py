import energies
import plot
import fit


def plot_name(label):
    return f'{energies.Files.plot_directory}{label}.pdf'


def Get_Experimental_Data(isotope, debug_mode=False):
    """Read the experimental data for a particular band sequence of an isotope.
    The data corresponds to the wobbling excitations of an isotope with a defined parity.
    """

    # DEBUG_MODE = False

    YRAST, TW1, LABEL = energies.Extract_Data.Get_Energies(isotope)
    EXP_DATA = fit.Fit.Concatenate_Data(YRAST, TW1)

    if(debug_mode):
        print(f'****** {LABEL} ******')
        print(f'****** Yrast band ******\n{YRAST}')
        print(f'****** TW1 band ******\n{TW1}')
        print(f'****** EXP DATA: ******\n{EXP_DATA}\n')

    X_DATA_SPINS = [X[0] for X in EXP_DATA]
    X_DATA_PHONONS = [X[1] for X in EXP_DATA]
    Y_DATA = [X[2] for X in EXP_DATA]

    if(debug_mode):
        print([X_DATA_SPINS], [X_DATA_PHONONS])
        print(Y_DATA)

    return [X_DATA_SPINS, X_DATA_PHONONS, Y_DATA]


def Au187_Pipeline():

    PLOT_FILE = plot_name('187Au')

    # data for $^{187}$Au - POSITIVE PARITY BANDS
    AU_187 = energies.Files.AU_187_DATA_NEGATIVE

    # get the experimental data for the positive parity wobbling bands
    x_data_1, x_data_2, y_data = Get_Experimental_Data(AU_187)

    print(x_data_1)
    print(x_data_2)
    print(y_data)


if __name__ == '__main__':
    Au187_Pipeline()
