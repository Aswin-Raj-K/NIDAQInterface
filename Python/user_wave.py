import numpy as np
import os

from wave import Wave


class UserWave(Wave):
    def __init__(self, Path, write_rate, freq=0, after_time=0):
        self.path = Path
        self.write_rate = write_rate
        self.array = self.get_text_data(Path)

    def get_array(self):
        # print(self.array)
        combined_array = np.array(self.array)
        return combined_array
    
    def get_freq(self):
        return len(1/(self.array*self.write_rate))

    @staticmethod
    def get_text_data(filename):
        array = []
        if os.path.exists(filename):
            file_read = open(filename, "r")
            for line in file_read.readlines():
                array.append(float(line))
        else:
            print("failed")
        file_read.close()
        return array


