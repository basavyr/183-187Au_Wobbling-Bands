import matplotlib.pyplot as plt
import os


class Plot_Maker:
    @staticmethod
    def Create_Plot(plot_file, data_set, label):
        x = [data_point[0] for data_point in data_set]
        y = [data_point[1] for data_point in data_set]

        fig, ax = plt.subplots()

        plt.plot(x, y, '-or', label=r'energies')
        plt.xlabel(r'$I\ [\hbar]$')
        plt.ylabel(r'$E\ [MeV]$')
        ax.legend(loc='best')
        plt.text(0.80, 0.20, f'{label}', horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=8)

        fig.tight_layout()
        plt.savefig(plot_file, bbox_inches='tight', dpi=1200)
        plt.close()

    @staticmethod
    def Create_Band_Plots(plot_file, data_set, plot_label):
        for data in data_set:
            print(data)

    @staticmethod
    def Clean_Plots(plot_file):
        try:
            os.remove(plot_file)
        except OSError:
            pass
