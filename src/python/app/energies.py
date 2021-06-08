import numpy as np
import plot


class Files:

    # main directory where everything is stored
    blobs = 'assets/'
    data_directory = blobs + 'data/'
    plot_directory = blobs + 'plots/'

    AU_183_DATA = data_directory + '183_data.md'
    AU_187_DATA = data_directory + '187_data.md'

    AU_183_ENERGY_PLOT = plot_directory + '183_energies_plot.pdf'
    AU_187_ENERGY_PLOT = plot_directory + '187_energies_plot.pdf'

    EXP_DATA_FILES = [AU_183_DATA, AU_187_DATA]
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
                band1.append([float(spin), float(energy)])
            if(int(parity) == 0):
                band0.append([float(spin), float(energy)])

        return band0, band1, label


class Energy_Formula:
    @staticmethod
    def Energy1(x, param1, param2, param3):
        y = param1 * x**2 + param2 * x + param3
        return y
