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
    def IsNAN_Asserter(arg, assert_value):
        try:
            assert np.isnan(arg) == assert_value
        except AssertionError:
            return None
        else:
            return arg

    @staticmethod
    def Inertia_Factor(MOI):
        return 1.0 / (2.0 * MOI)

    @staticmethod
    def Radians(angle):
        return angle * np.pi / 180.0

    @staticmethod
    def Energy1(x, param1, param2, param3):
        y = param1 * x**2 + param2 * x + param3
        return y

    @staticmethod
    def B_Term(spin, odd_spin, I1, I2, I3, V, gamma):

        A1 = Energy_Formula.Inertia_Factor(I1)
        A2 = Energy_Formula.Inertia_Factor(I2)
        A3 = Energy_Formula.Inertia_Factor(I3)

        I = spin
        j = odd_spin
        gm = Energy_Formula.Radians(gamma)
        rad3 = np.sqrt(3.0)
        cosg = np.cos(gm)
        sing = np.sin(gm)

        t1 = (2.0 * I - 1.0) * (A3 - A1) + 2.0 * j * A1
        t2 = (2.0 * I - 1.0) * (A2 - A1) + 2.0 * j * A1
        t3 = (2.0 * j - 1.0) * (A3 - A1) + 2.0 * I * A1 + V * \
            (2.0 * j - 1.0) / (j * (j + 1.0)) * rad3 * (rad3 * cosg + sing)
        t4 = (2.0 * j - 1.0) * (A2 - A1) + 2.0 * I * A1 + V * \
            (2.0 * j - 1.0) / (j * (j + 1.0)) * 2 * \
            rad3 * sing  # TODO check integrity for t4

        B = (t1 * t2) + (8.0 * A2 * A3 * I * j) + (t2 * t3)

        return -1.0 * B

    @staticmethod
    def C_Term(spin, odd_spin, I1, I2, I3, V, gamma):

        A1 = Energy_Formula.Inertia_Factor(I1)
        A2 = Energy_Formula.Inertia_Factor(I2)
        A3 = Energy_Formula.Inertia_Factor(I3)

        I = spin
        j = odd_spin
        gm = Energy_Formula.Radians(gamma)
        rad3 = np.sqrt(3.0)
        cosg = np.cos(gm)
        sing = np.sin(gm)

        # sub_term1
        t1_1 = (2.0 * I - 1.0) * (A3 - A1) + 2.0 * j * A1
        t1_2 = (2.0 * j) * (A3 - A1) + 2.0 * I * A1 + V * \
            (2.0 * j - 1.0) / (j * (j + 1.0)) * rad3 * (rad3 * cosg + sing)
        t1_3 = 4.0 * I * j * np.power(A3, 2)
        T1 = t1_1 * t1_2 - t1_3

        # sub_term2
        t2_1 = (2.0 * I - 1.0) * (A2 - A1) + 2.0 * j * A1
        t2_2 = (2.0 * j - 1.0) * (A2 - A1) + 2.0 * I * A1 + V * \
            (2.0 * j - 1.0) / (j * (j + 1.0)) * 2 * rad3 * sing
        t2_3 = 4.0 * I * j * np.power(A2, 2)
        T2 = t2_1 * t2_2 - t2_3

        C = T1 * T2

        return C

    @staticmethod
    def H_Min(spin, odd_spin, I1, I2, I3, V, gamma):

        A1 = Energy_Formula.Inertia_Factor(I1)
        A2 = Energy_Formula.Inertia_Factor(I2)
        A3 = Energy_Formula.Inertia_Factor(I3)

        I = spin
        j = odd_spin
        gm = Energy_Formula.Radians(gamma)
        pi6 = np.pi / 6.0
        sing = np.sin(gm)  # TODO check missing of the sing term

        T1 = (A2 + A3) * (I + j) / 2.0
        T2 = A1 * np.power(I - j, 2)
        T3 = V * (2.0 * j - 1.0) / (j + 1.0) * np.sin(pi6 + gm)

        HMIN = T1 + T2 - T3

        return HMIN

    @staticmethod
    def Omega_Frequencies(spin, odd_spin, I1, I2, I3, V, gamma):

        DEBUG_MODE = False

        B = Energy_Formula.B_Term(spin, odd_spin, I1, I2, I3, V, gamma)
        C = Energy_Formula.C_Term(spin, odd_spin, I1, I2, I3, V, gamma)

        with np.errstate(invalid='ignore'):
            SQRT = np.sqrt(np.power(B, 2) - 4.0 * C)
            if(DEBUG_MODE):
                print(
                    f'SQRT TERM -> {SQRT} | {Energy_Formula.IsNAN_Asserter(SQRT, False)}')

        with np.errstate(invalid='ignore'):
            Omega_1 = np.sqrt(0.5 * (-B + SQRT))
            valid_1 = Energy_Formula.IsNAN_Asserter(Omega_1, False)
            if(DEBUG_MODE):
                if(valid_1 is None):
                    print(f'Invalid Omega_1 | v1={valid_1}')
                else:
                    print(f'Valid Omega_1 | v1={valid_1}')

        with np.errstate(invalid='ignore'):
            Omega_2 = np.sqrt(0.5 * (-B - SQRT))
            valid_2 = Energy_Formula.IsNAN_Asserter(Omega_2, False)
            if(DEBUG_MODE):
                if(valid_2 is None):
                    print(f'Invalid Omega_2 | v2={valid_2}')
                else:
                    print(f'Valid Omega_2 | v2={valid_2}')

        if(valid_1 is None or valid_2 is None):
            if(DEBUG_MODE):
                print('Invalid parameters for the wobbling frequencies ❌')
                print(f'Omegas: -> [{Omega_1} , {Omega_2}]')
                return []
        else:
            if(DEBUG_MODE):
                print('Valid parameters for the wobbling frequencies ✅')
                print(f'Omegas: -> [{Omega_1} , {Omega_2}]')
            return [Omega_1, Omega_2]

    @staticmethod
    def Energy_Expression(nw_1, nw_2, spin, odd_spin, I1, I2, I3, V, gamma):

        h0 = Energy_Formula.H_Min(spin, odd_spin, I1, I2, I3, V, gamma)

        Omega = Energy_Formula.Omega_Frequencies(
            spin, odd_spin, I1, I2, I3, V, gamma)

        if(len(Omega) == 0):
            return None

        Omega_1 = Omega[0]
        Omega_2 = Omega[1]

        E = h0+Omega_1*(nw_1+0.5)+Omega_2*(nw_2+0.5)
        return E

    @staticmethod
    def Excitation_Energy(nw_1, nw_2, spin, spin_zero, odd_spin, I1, I2, I3, V, gamma):

        E_0 = Energy_Formula.Energy_Expression(
            0, 0, spin_zero, odd_spin, I1, I2, I3, V, gamma)

        E_I = Energy_Formula.Energy_Expression(
            nw_1, nw_2, spin, odd_spin, I1, I2, I3, V, gamma)

        E_EXC = E_I-E_0

        return E_EXC
