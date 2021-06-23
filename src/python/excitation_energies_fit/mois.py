import numpy as np

import matplotlib.pyplot as plt


class MOI:

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


def Plot_MOIs(moi_type):
    plot_file = f'./assets/plots/{moi_type.__name__}_MOIS.pdf'
    print(plot_file)


if __name__ == '__main__':
    # mois = MOI.Irrotational(30, 15)
    # print(mois)
    Plot_MOIs(MOI.Irrotational)
