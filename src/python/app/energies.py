

class Extract_Data:
    def Get_Energies(data_file):
        band0 = []
        band1 = []
        with open(data_file, 'r+') as data_reader:
            raw_data = data_reader.readlines()

        raw_data.pop(0)
        return raw_data


