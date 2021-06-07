import energies
import fit


def Main():
    for isotope in energies.Files.EXP_DATA_FILES:
        isotope_data = energies.Extract_Data.Get_Energies(isotope)
        print(f'Nucleus -> {isotope_data[2]}')

        # first band
        band_0 = isotope_data[0]
        # generate x_data
        band_0_spins = [x[0] for x in band_0]
        # generate y_data
        band_0_energies = [x[1] for x in band_0]

        #second band

if __name__ == '__main__':
    Main()
