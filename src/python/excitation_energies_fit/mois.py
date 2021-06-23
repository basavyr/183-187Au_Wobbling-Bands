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
        sin_squared = lambda x: np.power(np.sin(x), 2)
        gm_rad = MOI.Rad(gm)
        PI3 = np.pi / 3.0
        SIN_ARGS = [gm_rad - 2 * PI3 * k for k in range(1, 4)]

        pure_mois = list(map(sin_squared, SIN_ARGS))
        return pure_mois


if __name__ == '__main__':
    mois = MOI.Irrotational(1, 1)
    print(mois)
