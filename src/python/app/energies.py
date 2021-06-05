import plot

AU_183_FILE = '183_data.md'
AU_187_FILE = '187_data.md'

AU_183_ENERGY_PLOT = '183_energies_plot.pdf'
AU_187_ENERGY_PLOT = '187_energies_plot.pdf'


EXP_DATA = [AU_183_FILE, AU_187_FILE]
PLOT_FILES = [AU_183_ENERGY_PLOT, AU_187_ENERGY_PLOT]


class Extract_Data:

    @staticmethod
    def Get_Energies(data_file):
        band0 = []
        band1 = []

        with open(data_file, 'r+') as data_reader:
            raw_data = data_reader.readlines()

        label = str(raw_data[0]).strip()

        raw_data.pop(0)

        clean_data = [line.strip() for line in raw_data]

        for line in clean_data:
            parity, spin, energy = line.split(" ")
            if(int(parity) == 1):
                band1.append([spin, energy])
            if(int(parity) == 0):
                band0.append([spin, energy])

        return band0, band1, label


def Main():
    clean = True
    count = 0
    for data in EXP_DATA:
        w_data = Extract_Data.Get_Energies(data)
        plot_label = w_data[2]
        data_set = [w_data[0], w_data[1]]
        print(plot_label)
        plot.Plot_Maker.Create_Band_Plots(PLOT_FILES[count], data_set, plot_label)
        count += 1

    if(clean):
        for file in PLOT_FILES:
            plot.Plot_Maker.Clean_Plots(file)


if __name__ == '__main__':
    Main()
