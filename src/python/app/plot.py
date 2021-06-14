import matplotlib.pyplot as plt
import os


class Plot_Maker:
    @staticmethod
    def Create_Plot(plot_file, data_set, plot_label):
        x = [data_point[0] for data_point in data_set]
        y = [data_point[1] for data_point in data_set]

        fig, ax = plt.subplots()

        plt.plot(x, y, '-or', label=r'$E_w$')
        ax.set_title(f'Wobbling energies for {plot_label}')
        plt.xlabel(r'$I\ [\hbar]$')
        plt.ylabel(r'$E\ [MeV]$')
        ax.legend(loc='best')
        plt.text(0.80, 0.20, f'{plot_label}', horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=11)

        fig.tight_layout()
        plt.savefig(plot_file, bbox_inches='tight', dpi=1200)
        plt.close()

    @staticmethod
    def Create_Band_Plots(plot_file, data_set, plot_label):
        fig, ax = plt.subplots()
        band_counter = 1

        for data in data_set:
            x = [data_point[0] for data_point in data]
            y = [data_point[1] for data_point in data]

            plt.plot(x, y, '-or', label=f'Band-{band_counter}')
            band_counter += 1

        plt.xlabel(r'$I\ [\hbar]$')
        plt.ylabel(r'$E\ [MeV]$')
        ax.legend(loc='best')
        ax.set_title(f'Wobbling energies for {plot_label}')
        plt.text(0.80, 0.20, f'{plot_label}', horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=11)

        plt.savefig(plot_file, bbox_inches='tight', dpi=400)
        fig.tight_layout()
        plt.close()

    @staticmethod
    def Create_Fit_Plot(expdata, thdata, plot_file, plot_label):
        # the experimental results -> spins
        x_data_exp = expdata[0]
        # the experimental results -> energies
        y_data_exp = expdata[1]

        # the theoretical results -> spins
        x_data_th = thdata[0]
        # the theoretical results -> energies
        y_data_th = thdata[1]

        fig, ax = plt.subplots()

        # plot the experimental curve
        plt.plot(x_data_exp, y_data_exp, 'ok', label='Exp')
        # plot the theoretical curve
        plt.plot(x_data_th, y_data_th, '-r', label='Th')

        plt.xlabel(r'$I\ [\hbar]$')
        plt.ylabel(r'$E\ [MeV]$')
        ax.legend(loc='best')
        ax.set_title(f'Wobbling energies for {plot_label}')

        plt.text(0.80, 0.20, f'{plot_label}', horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=11)

        plt.savefig(plot_file, bbox_inches='tight', dpi=400)
        fig.tight_layout()
        plt.close()

    @staticmethod
    def Plot_Bands(band1, band2, plot_file, plot_label):
        # create the data sets for the first band
        xdata_b1 = band1[0]
        ydata_b1_exp = band1[1]
        ydata_b1_th = band1[2]

        # create the data sets for the second band
        xdata_b2 = band2[0]
        ydata_b2_exp = band2[1]
        ydata_b2_th = band2[2]

        fig, ax = plt.subplots()

        # plot the experimental curve for the first band
        plt.plot(xdata_b1, ydata_b1_exp, 'ok', label='Yrast-Exp')
        # plot the theoretical curve for the first band
        plt.plot(xdata_b1, ydata_b1_th, '-r', label='Yrast-Th')

        # plot the experimental curve for the second band
        plt.plot(xdata_b2, ydata_b2_exp, '+k', label='TW1-Exp')
        # plot the theoretical curve for the second band
        plt.plot(xdata_b2, ydata_b2_th, '-b', label='TW1-Th')

        plt.xlabel(r'$I\ [\hbar]$')
        plt.ylabel(r'$E\ [MeV]$')
        ax.legend(loc='best')
        ax.set_title(f'Wobbling energies: {plot_label}')

        plt.text(0.80, 0.20, f'{plot_label}', horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=11)

        plt.savefig(plot_file, bbox_inches='tight', dpi=400)
        fig.tight_layout()
        plt.close()

    @staticmethod
    def Clean_Plots(plot_file):
        try:
            os.remove(plot_file)
        except OSError:
            pass
