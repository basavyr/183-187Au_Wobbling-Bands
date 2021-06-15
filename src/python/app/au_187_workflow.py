import energies
import plot
import fit


def plot_name(label):
    return f'{energies.Files.plot_directory}{label}.pdf'


def Get_Experimental_Data(isotope, debug_mode=False):
    """Read the experimental data for a particular band sequence of an isotope.
    The data corresponds to the wobbling excitations of an isotope with a defined parity.
    """

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


def Fit_Model(model_function, initial_params, param_bounds, x_data_1, x_data_2, y_data, debug_mode=False):

    spins = energies.np.asarray(x_data_1)
    wobbling_phonons = energies.np.asarray(x_data_2)

    # evaluation of the excitation energy for all the spins and wobbling phonon numbers of the band
    # this is a 1-D array that results from applying E_exc on the entire set of spins and wobbling phonons
    exp_data = energies.np.asarray(y_data)

    band_head = exp_data[0]

    # normalize the experimental data to the band-head
    exp_data_normed = [e - band_head for e in exp_data]

    # Use the curve_fit function to find the best parameter set for the current experimental data-set
    # the curve fit uses the analytical expression of the band as a model function
    # the X-data is a tuple of arrays: the spins and wobbling phonon numbers
    # the fitting procedure uses an initial set of parameters (guessed values)
    # the fitting procedure adopts fixed bounds
    fit_results = fit.curve_fit(
        model_function, (spins, wobbling_phonons), exp_data_normed, p0=initial_params, bounds=param_bounds)  # Pure curve_fit procedure applied on the data

    # retreive the parameter set from the fitting results (unpacked value)
    params = fit_results[0]
    params = [round(p, 3) for p in params]
    if(debug_mode):
        print(params)

    th_data = model_function(
        (spins, wobbling_phonons), params[0], params[1], params[2], params[3], params[4])
    th_data = [round(th, 3) for th in th_data]
    if(debug_mode):
        print(f'Theoretical Data-> {th_data}')

    # extract the theoretical data for the band1 and band2
    th_data_1 = []
    th_data_2 = []
    for idx in range(len(wobbling_phonons)):
        if(wobbling_phonons[idx] == 0):
            th_data_1.append(th_data[idx])
        else:
            th_data_2.append(th_data[idx])

    rms_value = fit.Fit.RMS(exp_data_normed, th_data)
    if(debug_mode):
        print(f'RMS -> {rms_value}')

    return [th_data_1, th_data_2], params, rms_value


def Au187_Pipeline(initial_params, debug_mode=False):

    # PLOT_FILE = plot_name('187Au')

    # data for $^{187}$Au - POSITIVE PARITY BANDS
    AU_187 = energies.Files.AU_187_DATA_NEGATIVE

    # get the experimental data for the positive parity wobbling bands
    x_data_1, x_data_2, y_data = Get_Experimental_Data(AU_187)

    # fit_results=Fit_Model()


if __name__ == '__main__':
    initial_params = [60, 20, 5, 2.1, 21]
    Au187_Pipeline(initial_params)
