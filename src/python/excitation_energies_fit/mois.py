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
        gm_rad = MOI.Rad(gm)
        k = 1
        return k


if __name__ == '__main__':
    MOI.Irrotational(1,1)