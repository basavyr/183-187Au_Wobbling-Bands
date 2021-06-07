import energies
import fit


def Main():
    for isotope in energies.Files.EXP_DATA_FILES:
        isotope_data = energies.Extract_Data.Get_Energies(isotope)
        print(f'Nucleus -> {isotope_data[2]}')


if __name__ == '__main__':
    Main()
