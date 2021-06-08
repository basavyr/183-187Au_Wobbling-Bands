import energies
import fit
import plot


class Isotope:

    @staticmethod
    def Fit_Isotope(data):
        # spins
        # x_data = data[0]
        # energies (experimental energies)
        # ydata = data[1]

        try:
            nlm = fit.Mock_Fit.Fit(data, energies.Energy_Formula.Energy1)
        except Exception:
            nlm = -1
            return nlm
        else:
            return nlm


def Main():

    model = energies.Energy_Formula.Energy1

    def plot_name(idx): return f'fit_results_{idx}.pdf'

    idx = 1

    for isotope in energies.Files.EXP_DATA_FILES:
        isotope_data = energies.Extract_Data.Get_Energies(isotope)

        plot_label = isotope_data[2]
        print(f'Nucleus -> {plot_label}')

        # first band
        band_0 = isotope_data[0]
        print(band_0)
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
        nlm_1 = Isotope.Fit_Isotope(data_1)

        print(nlm_0[0])

        exp_data = [band_0_spins, band_0_energies]
        th_data = [band_0_spins, fit.Mock_Fit.Check_Mock_Data(
            model, band_0_spins, nlm_0[0])]

        plot.Plot_Maker.Create_Fit_Plot(
            exp_data, th_data, f'assets/plots/{plot_name(idx)}', plot_label)

        idx += 1
        # print(band_1_energies)
        # print(fit.Mock_Fit.Check_Mock_Data(model, band_1_spins, nlm_1[0]))


def none(arg):
    x = arg
    try:
        assert x == 1
    except Exception:
        return None
    else:
        return [1, 2]


if __name__ == '__main__':
    print(none(-1))
