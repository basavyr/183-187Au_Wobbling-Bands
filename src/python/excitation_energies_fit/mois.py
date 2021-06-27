import numpy as np

import matplotlib.pyplot as plt


class MOI:
    plot_file = lambda moi_type: f'./assets/plots/{moi_type.__name__}_MOIS.pdf'
    plot_bundle_file = lambda file: f'./assets/plots/{file}.pdf'

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
        plt.title(f'{moi_type.__name__} - Moments of Inertia')
        plt.xlabel(r'$\gamma$ [deg]')
        plt.ylabel(r'$\mathcal{I}$ [$\hbar^2/MeV$]]')
        plt.legend(loc='best')
        plt.savefig(plot_file, bbox_inches='tight', dpi=300)
        plt.close()

    @staticmethod
    def Plot_Rigid_MOIs(plot_file, moi_type, I0, beta):
        # define the limits of the gamma parameter (in degrees)
        gamma_limits = [0, 60]
        # define the step of the x-data (in degrees)
        x_data_step = 5
        x_data = np.arange(
            gamma_limits[0], gamma_limits[1] + x_data_step, x_data_step)

        moi_data = [moi_type(I0, x, beta) for x in x_data]

        i1_data = [x[0] for x in moi_data]
        i2_data = [x[1] for x in moi_data]
        i3_data = [x[2] for x in moi_data]

        fig, ax = plt.subplots()

        plot_label = r'$\mathcal{I}_0$' + \
            f' = {I0}' + '\n' + r'$\beta=$' + f' ={beta}'
        plt.text(0.25, 0.65, plot_label, horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=8)

        plt.plot(x_data, i1_data, '-r', label=r'$\mathcal{I}_1$')
        plt.plot(x_data, i2_data, '-k', label=r'$\mathcal{I}_2$')
        plt.plot(x_data, i3_data, '-b', label=r'$\mathcal{I}_3$')
        plt.title(f'{moi_type.__name__} - Moments of Inertia')
        plt.xlabel(r'$\gamma$ [deg]')
        plt.ylabel(r'$\mathcal{I}$ [$\hbar^2/MeV$]]')
        plt.legend(loc='best')
        try:
            plt.savefig(plot_file, bbox_inches='tight', dpi=300)
        except Exception:
            pass
        plt.close()

    @staticmethod
    def Plot_Axes(plot_file, axis, I0, beta):
        gm_step = 5
        x_data = np.arange(0, 60 + gm_step, gm_step)
        y_rigid = [MOI.Rigid(I0, x, beta)[axis] for x in x_data]
        y_hydro = [MOI.Hydrodynamic(I0, x)[axis] for x in x_data]
        # y_data3 = [MOI.Irrotational(I0, x)[axis] for x in x_data]

        fig, ax = plt.subplots()

        plot_label = r'$\mathcal{I}_0$' + \
            f' = {I0}' + '\n' + r'$\beta=$' + f' ={beta}'
        plt.text(0.25, 0.65, plot_label, horizontalalignment='center',
                 verticalalignment='center', transform=ax.transAxes, fontsize=8)

        plt.plot(x_data, y_rigid, '-r', label=f'Rigid-Like')
        plt.plot(x_data, y_hydro, '-k', label=f'Hydro-Like')
        # plt.plot(x_data, i3_data, '-b', label=r'$\mathcal{I}_3$')
        # plt.title(f'{moi_type.__name__} - Moments of Inertia')
        plt.xlabel(r'$\gamma$ [deg]')
        plt.ylabel(r'$\mathcal{I}$ [$\hbar^2/MeV$]]')
        plt.legend(loc='best')
        plt.savefig(plot_file, bbox_inches='tight', dpi=300)
        plt.close()

    @staticmethod
    def Plot_Bundle(plot_file, axis, *params):
        do_plot = True
        try:
            assert axis == 1 or axis == 2 or axis == 3, 'Wrong axes'
        except AssertionError as err:
            print(err)
            do_plot = False
        else:
            do_plot = True
        if(do_plot):
            param_size = len(params)
            if(param_size == 2):
                I0 = params[0]
                beta = params[1]
                MOI.Plot_Axes(plot_file, axis, I0, beta)
            else:
                print('Cannot plot the three MOIs')

    @ staticmethod
    def InertiaFactor(MOI):
        return 1.0 / (2.0 * MOI)

    @ staticmethod
    def Rad(angle):
        return angle * np.pi / 180.0

    @ staticmethod
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

    @ staticmethod
    def Hydrodynamic(I0, gm):
        # define the trigonometric function for generating the un-normalized moments of inertia
        sin_squared = lambda x: np.power(np.sin(x), 2)

        # transform the angle into radians from degrees
        gm_rad = MOI.Rad(gm)
        PI3 = np.pi / 3.0

        # generate the tuple of arguments that go inside the trigonometric function
        SIN_ARGS = [gm_rad + 2 * PI3 * k for k in range(1, 4)]

        # apply the trigonometric function to the list of tuples
        pure_mois = list(map(sin_squared, SIN_ARGS))

        # return the normalized moments of inertia
        mois = list(map(lambda x: (4.0 / 3.0 * I0) * x, pure_mois))
        return mois

    @ staticmethod
    def Rigid(I0, gm, beta):
        # transform gamma from degrees into radians
        gm_rad = MOI.Rad(gm)

        pi_5_16 = 5.0 / (16.0 * np.pi)
        pi_5_4 = 5.0 / (4.0 * np.pi)
        pi_2_3 = 2.0 / 3.0 * np.pi

        COS_ARGS = [np.cos(gm_rad + pi_2_3 * k) for k in range(1, 4, 1)]
        COS_TERMS = [1 - np.sqrt(pi_5_4) * beta * x for x in COS_ARGS]

        C_BETA = 1.0 + np.sqrt(pi_5_16) * beta
        CONST = float(I0 / C_BETA)

        RESULT_TUPLE = [CONST * x for x in COS_TERMS]
        return RESULT_TUPLE


if __name__ == '__main__':
    # MOI.Plot_MOIs(MOI.plot_file(MOI.Irrotational), MOI.Irrotational, 10)
    # MOI.Plot_MOIs(MOI.plot_file(MOI.Hydrodynamic), MOI.Hydrodynamic, 10)
    # MOI.Plot_Rigid_MOIs(MOI.plot_file(MOI.Rigid), MOI.Rigid, 10, 0.3)
    MOI.Plot_Bundle(MOI.plot_bundle_file('moi_1'), 1, 25, 0.3)
