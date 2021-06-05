

AU_183_FILE = '183_data.md'
AU_187_FILE = '187_data.md'


class Extract_Data:

    @staticmethod
    def Get_Energies(data_file):
        band0 = []
        band1 = []

        with open(data_file, 'r+') as data_reader:
            raw_data = data_reader.readlines()

        raw_data.pop(0)

        clean_data = [line.strip() for line in raw_data]

        for line in clean_data:
            parity, spin, energy = line.split(" ")
            if(int(parity) == 1):
                band1.append([spin, energy])
            if(int(parity) == 0):
                band0.append([spin, energy])

        return band0, band1


def Main():
    w = Extract_Data.Get_Energies(AU_183_FILE)
    print(w[0])
    print(w[1])


if __name__ == '__main__':
    Main()
