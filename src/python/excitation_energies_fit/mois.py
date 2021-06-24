import numpy as np

import matplotlib.pyplot as plt


class MOI:
    @staticmethod
    def Plot_MOIs(plot_file, moi_type, I0):
        # define the limits of the gamma parameter (in degrees)
        gamma_limits = [0, 60]
        # define the step of the x-data (in degrees)
        x_data_step = 5
        x_data = np.arange(
            gamma_limits[0], gamma_limits[1] + x_data_step, x_data_step)

        moi_data = [moi_type(I0, x) for x in x_data]

        i1_data = [x[0] for x in moi_data]
        i2_data = [x[1] for x in moi_data]
        i3_data = [x[2] for x in moi_data]

        fig, ax = plt.subplots()

        plot_label = r'$\mathcal{I}_0$' + f' = {I0}'
        plt.text(0.25, 0.65, plot_label, horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=8)

        plt.plot(x_data, i1_data, '-r', label=r'$\mathcal{I}_1$')
        plt.plot(x_data, i2_data, '-k', label=r'$\mathcal{I}_2$')
        plt.plot(x_data, i3_data, '-b', label=r'$\mathcal{I}_3$')
        plt.xlabel(r'$\gamma$ [deg]')
        plt.ylabel(r'$\mathcal{I}$ [$\hbar^2/MeV$]]')
        plt.legend(loc='best')
        plt.savefig(plot_file, bbox_inches='tight', dpi=300)
        plt.close()

    @staticmethod
    def InertiaFactor(MOI):
        return 1.0 / (2.0 * MOI)

    @staticmethod
    def Rad(angle):
        return angle * np.pi / 180.0

    @staticmethod
    def Irrotational(I0, gm):
        # define the trigonometric function for generating the un-normalized moments of inertia
        sin_squared = lambda x: np.power(np.sin(x), 2)

        # transform the angle into radians from degrees
        gm_rad = MOI.Rad(gm)
        PI3 = np.pi / 3.0

        # generate the tuple of arguments that go inside the trigonometric function
        SIN_ARGS = [gm_rad - 2 * PI3 * k for k in range(1, 4)]

        # apply the trigonometric function to the list of tuples
        pure_mois = list(map(sin_squared, SIN_ARGS))

        # return the normalized moments of inertia
        mois = list(map(lambda x: I0 * x, pure_mois))
        return mois


if __name__ == '__main__':
    plot_file = lambda moi_type: f'./assets/plots/{moi_type.__name__}_MOIS.pdf'
    MOI.Plot_MOIs(plot_file(MOI.Irrotational), MOI.Irrotational, 10)
