import matplotlib.pyplot as plt


class Plot_Maker:
    @staticmethod
    def Create_Plot(plot_file, data_set):
        x = [data_point[0] for data_point in data_set]
        y = [data_point[1] for data_point in data_set]

        plt.plot(x, y, '-or', label=r'energies')
        plt.xlabel(r'$I[\hbar]$')
        plt.ylabel(r'$E[MeV]$')
        plt.legend(loc='best')
        plt.savefig(plot_file, bbox_inches='tight', dpi=1200)
        plt.close()
