import energies
import fit


def Main():
    for isotope in energies.Files.EXP_DATA_FILES:
        isotope_data = energies.Extract_Data.Get_Energies(isotope)
        print(f'Nucleus -> {isotope_data[2]}')
        # generate xdata
        spins_data = [x[0] for x in isotope_data[0]]
        # generate ydata
        energy_data = [x[1] for x in isotope_data[0]]
        print(spins_data)
        print(energy_data)


if __name__ == '__main__':
    Main()
