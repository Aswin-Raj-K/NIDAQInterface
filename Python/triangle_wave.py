import numpy as np

#from wave import Wave


class TriangleWave():  # min is simply the starting and ending value and max is the peak/trough value
    def __init__(self, Min, Max, Ramp_Rate, samp_freq, Freq=0, after_time=0):
        self.min = float(Min)
        self.max = float(Max)
        self.samp_freq = int(samp_freq)
        if (Ramp_Rate == 0) or ((Min == 0) and (Max == 0)):
            self.min = 0
            self.max = 2
            self.slope = 400
            self.zero_wave = True
        else:
            self.slope = Ramp_Rate
            self.zero_wave = False
        self.freq = Freq

        if self.zero_wave == False:
            if Freq > 0:
                if 1 / Freq < (abs(self.max - self.min) / self.slope) * 2:
                    raise Exception("Frequency is too high. Max with current parameters is: {} Hz.".format(
                       1 / ((abs(self.max - self.min) / self.slope) * 2)))
                else:
                    self.after_t = (1 / Freq) - ((abs(self.max - self.min) / self.slope) * 2)
            else:
                self.after_t = after_time

        self.num_points_action = (abs(self.max - self.min) / self.slope) * self.samp_freq * 2
        self.num_points_after = 0

    def get_array(self):
        # pre_array = np.linspace(self.min, self.min, self.num_points_pre)

        action_array = self.generate_tri(self.min, self.max, self.num_points_action)
        if self.freq > 0:   
            self.num_points_after = int(((1/self.freq)*self.samp_freq)-len(action_array))
        after_array = np.linspace(self.min, self.min, self.num_points_after)

        combined_array = np.append(action_array, after_array)
        if self.zero_wave:
            return np.linspace(0.0,0.0,len(combined_array))
        else:
            return combined_array
        
     
    def get_voltage_high(self): #DM new
        voltage_high = self.max
        return voltage_high
    def get_voltage_low(self): #DM new
        voltage_low = self.min
        return min
    def get_ramp_rate(self): #DM new
        return ramp_rate
    def get_repetition_rate(self): #DM new
        self.samp_freq = int(samp_freq)
        repetition_rate = self.samp_freq
        return repetition_rate
        

    @staticmethod
    def generate_tri(minimum, maximum, number_points):
        if number_points % 2 == 0:
            slope_1 = np.arange(minimum, maximum, (maximum - minimum) / ((number_points / 2)))
            # slope_1 = np.linspace(minimum, maximum, number_points)
            slope_2 = np.flip(slope_1)
            slope_1 = np.append(slope_1, np.array([maximum]))
        else:
            slope_1 = np.arange(minimum, maximum, (maximum - minimum) / (number_points // 2))
            # slope_1 = np.linspace(minimum, maximum, number_points)
            slope_2 = np.flip(slope_1)
            slope_1 = np.append(slope_1, np.array([maximum]))
        action_array = np.append(slope_1, slope_2)
        return action_array
    
    def get_freq(self):
        return self.freq

if __name__ == "__main__":
    test = TriangleWave(-0.4,1.3,400,20000,10)
    test2= TriangleWave(-0.8,2.6,800,20000,60,0)
