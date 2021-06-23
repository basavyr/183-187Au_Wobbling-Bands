import numpy as np
import plot


class Files:

    # main directory where everything is stored
    blobs = 'assets/'
    data_directory = blobs + 'data/'
    plot_directory = blobs + 'plots/'

    # store the experimental data for 183Au
    AU_183_DATA_POSITIVE = data_directory + '183_positive_data.md'
    AU_183_DATA_NEGATIVE = data_directory + '183_negative_data.md'
    # store the experimental data for 187Au
    # AU_187_DATA_POSITIVE = data_directory + '187_positive_data.md'
    AU_187_DATA_NEGATIVE = data_directory + '187_negative_data.md'

    # store the plots for 183Au
    AU_183_POSITIVE_ENERGY_PLOT = plot_directory + '183_positive_energies_plot.pdf'
    AU_183_NEGATIVE_ENERGY_PLOT = plot_directory + '183_negative_energies_plot.pdf'
    # store the plots for 187Au
    # AU_187_POSITIVE_ENERGY_PLOT = plot_directory + '187_positive_energies_plot.pdf'
    AU_187_NEGATIVE_ENERGY_PLOT = plot_directory + '187_negative_energies_plot.pdf'

    AU_183_POSITIVE_FIT_DATA = data_directory + '183_Positive_Fit_Data.dat'
    AU_183_NEGATIVE_FIT_DATA = data_directory + '183_Negative_Fit_Data.dat'
    AU_187_FIT_DATA = data_directory + '187_Fit_Data.dat'


class Extract_Data:

    @staticmethod
    def Get_Energies(data_file):
        YRAST = []
        TW1 = []

        with open(data_file, 'r+') as data_reader:
            raw_data = data_reader.readlines()

        label = str(raw_data[0]).strip()

        raw_data.pop(0)

        clean_data = [line.strip() for line in raw_data]

        for line in clean_data:
            wobbling_phonon, spin, energy = line.split(" ")
            if(int(wobbling_phonon) == 1):
                TW1.append(
                    [float(spin), int(wobbling_phonon), float(energy)])
            if(int(wobbling_phonon) == 0):
                YRAST.append(
                    [float(spin), int(wobbling_phonon), float(energy)])

        return YRAST, TW1, label


class Energy_Formula:

    FAIL_VALUE = 6969.6969

    @staticmethod
    def MeV(band):
        band = [[e[0], e[1], float(e[2] / 1000.0)] for e in band]
        return band

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
            rad3 * sing

        B = (t1 * t2) + (8.0 * A2 * A3 * I * j) + (t3 * t4)

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
        t1_2 = (2.0 * j - 1.0) * (A3 - A1) + 2.0 * I * A1 + V * \
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

        T1 = (A2 + A3) * (I + j) / 2.0
        T2 = A1 * np.power(I - j, 2)
        T3 = V * (2.0 * j - 1.0) / (j + 1.0) * np.sin(pi6 + gm)

        H_MIN = T1 + T2 - T3

        return H_MIN

    @staticmethod
    def Omega_Frequencies(spin, odd_spin, I1, I2, I3, V, gamma, reversed=False):

        B = Energy_Formula.B_Term(spin, odd_spin, I1, I2, I3, V, gamma)
        C = Energy_Formula.C_Term(spin, odd_spin, I1, I2, I3, V, gamma)

        with np.errstate(invalid='ignore'):
            SQRT = np.sqrt(np.power(B, 2) - 4.0 * C)
            Omega_1 = np.sqrt(0.5 * (-B + SQRT))
            Omega_2 = np.sqrt(0.5 * (-B - SQRT))

        # with np.errstate(invalid='ignore'):
        #     SQRT = np.sqrt(np.power(B, 2) - 4.0 * C)
        #     valid_0 = Energy_Formula.IsNAN_Asserter(SQRT, False)
        #     if(DEBUG_MODE):
        #         if(valid_0 is None):
        #             print(f'Invalid SQRT term | v0={valid_0}')
        #         else:
        #             print(f'Valid SQRT term | v0={valid_0}')

        # if(valid_0 is None):
        #     return []

        # with np.errstate(invalid='ignore'):
        #     Omega_1 = np.sqrt(0.5 * (-B + SQRT))
        #     valid_1 = Energy_Formula.IsNAN_Asserter(Omega_1, False)
        #     if(DEBUG_MODE):
        #         if(valid_1 is None):
        #             print(f'Invalid Omega_1 | v1={valid_1}')
        #         else:
        #             print(f'Valid Omega_1 | v1={valid_1}')

        # with np.errstate(invalid='ignore'):
        #     Omega_2 = np.sqrt(0.5 * (-B - SQRT))
        #     valid_2 = Energy_Formula.IsNAN_Asserter(Omega_2, False)
        #     if(DEBUG_MODE):
        #         if(valid_2 is None):
        #             print(f'Invalid Omega_2 | v2={valid_2}')
        #         else:
        #             print(f'Valid Omega_2 | v2={valid_2}')

        # if(valid_1 is None or valid_2 is None):
        #     if(DEBUG_MODE):
        #         print('Invalid parameters for the wobbling frequencies ❌')
        #         print(f'Omegas: -> [{Omega_1} , {Omega_2}]')
        #         return []
        # else:
        #     if(DEBUG_MODE):
        #         print('Valid parameters for the wobbling frequencies ✅')
        #         print(f'Omegas: -> [{Omega_1} , {Omega_2}]')
        #     return [Omega_1, Omega_2]
        if(reversed):
            return [Omega_2, Omega_1]
        else:
            return [Omega_1, Omega_2]

    @staticmethod
    def Energy_Expression(nw_1, nw_2, spin, odd_spin, I1, I2, I3, V, gamma):

        H_MIN = Energy_Formula.H_Min(spin, odd_spin, I1, I2, I3, V, gamma)

        # Use the reversed variable for the wobbling frequency ordering.
        # Depending on its value, the frequencies will be interchanged for further computations
        reversed = False
        Omega_1, Omega_2 = Energy_Formula.Omega_Frequencies(
            spin, odd_spin, I1, I2, I3, V, gamma, reversed)

        # print(Omega_1)
        # print(Omega_2)

        E = H_MIN + Omega_1 * (nw_1 + 0.5) + Omega_2 * (nw_2 + 0.5)
        return E

    @staticmethod
    def Excitation_Energy(nw_1, nw_2, spin, spin_zero, odd_spin, I1, I2, I3, V, gamma):
        """
        Calculates the wobbling energy of a state with given spin, belonging to a particular band, by subtracting from its absolute value the value of the yrast band-head state with I=spin_zero.
        """

        E_0 = Energy_Formula.Energy_Expression(
            0, 0, spin_zero, odd_spin, I1, I2, I3, V, gamma)

        E_I = Energy_Formula.Energy_Expression(
            nw_1, nw_2, spin, odd_spin, I1, I2, I3, V, gamma)

        E_EXC = E_I - E_0

        return E_EXC


class Models:

    @staticmethod
    def Model_Energy_h9_2(X, P_1, P_2, P_3, P_4, P_5):
        """
        Describes the analytical expressions for the energies that correspond to the negative parity states.
        This is the model function that needs to be numerically fitted.

        The argument X represents the spin I and the wobbling phonon number n_w -> X = [I, n_w1].

        P represents the parameter set: P = [I1, I2, I3, V, gamma].
        """
        DEBUG_MODE = False

        # The band head of the negative parity sequences
        # Band head corresponds to the first level of the yrast band
        SPIN_ZERO = 4.5
        # The odd single-particle angular momentum which couples to the triaxial even-even core
        ODD_SPIN = 4.5

        # unpack the spin and wobbling phonon number
        spins, phonons = X

        if(DEBUG_MODE):
            print(f'in model ->Spins: {spins}\n nw_1: {phonons}')

        model_function = Energy_Formula.Excitation_Energy(
            phonons, 0, spins, SPIN_ZERO, ODD_SPIN, P_1, P_2, P_3, P_4, P_5)

        if(DEBUG_MODE):
            print(f'E_EXC(X,P) -> {model_function}')
        return model_function

    @staticmethod
    def Model_Energy_i13_2(X, P_1, P_2, P_3, P_4, P_5):
        """
        Describes the analytical expressions for the energies that correspond to the positive parity states.
        This is the model function that needs to be numerically fitted.

        The argument X represents the spin I and the wobbling phonon number n_w -> X = [I, n_w1].

        P represents the parameter set: P = [I1, I2, I3, V, gamma].
        """
        DEBUG_MODE = False

        # The band head of the positive parity sequences
        # Band head corresponds to the first level of the yrast band
        SPIN_ZERO = 6.5
        # The odd single-particle angular momentum which couples to the triaxial even-even core
        ODD_SPIN = 6.5

        # unpack the spins and the wobbling phonon numbers from the experimental data of the band
        spins, phonons = X

        if(DEBUG_MODE):
            print(f'in model ->Spins: {spins}\n nw_1: {phonons}')

        model_function = Energy_Formula.Excitation_Energy(
            phonons, 0, spins, SPIN_ZERO, ODD_SPIN, P_1, P_2, P_3, P_4, P_5)

        if(DEBUG_MODE):
            print(f'E_EXC(X,P) -> {model_function}')
        return model_function

    @staticmethod
    def Model_Energy_i11_2(X, P_1, P_2, P_3, P_4, P_5):
        """
        Describes the analytical expressions for the energies that correspond to the positive parity states.
        This is the model function that needs to be numerically fitted.

        The argument X represents the spin I and the wobbling phonon number n_w -> X = [I, n_w1].

        P represents the parameter set: P = [I1, I2, I3, V, gamma].
        """
        DEBUG_MODE = False

        # The band head of the positive parity sequences
        # Band head corresponds to the first level of the yrast band
        SPIN_ZERO = 4.5
        # The odd single-particle angular momentum which couples to the triaxial even-even core
        ODD_SPIN = 5.5

        # unpack the spins and the wobbling phonon numbers from the experimental data of the band
        spins, wobbling_phonons = X

        if(DEBUG_MODE):
            print(f'in model ->Spins: {spins}\n nw_1: {wobbling_phonons}')

        model_function = Energy_Formula.Excitation_Energy(
            wobbling_phonons, 0, spins, SPIN_ZERO, ODD_SPIN, P_1, P_2, P_3, P_4, P_5)

        if(DEBUG_MODE):
            print(f'E_EXC(X,P) -> {model_function}')
        return model_function
