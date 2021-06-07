import energies
import fit


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

    for isotope in energies.Files.EXP_DATA_FILES:
        isotope_data = energies.Extract_Data.Get_Energies(isotope)
        print(f'Nucleus -> {isotope_data[2]}')

        # first band
        band_0 = isotope_data[0]
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

        print(band_0_energies)
        print(fit.Mock_Fit.Check_Mock_Data(model, band_0_spins, nlm_0[0]))


if __name__ == '__main__':
    Main()
