class Writer:
    def __init__(self, num, name, waveform):
        self.num = num
        self.name = name
        self.waveform = waveform

    def get_array(self):
        array = self.waveform.get_array()
        return array
    
    def get_freq(self):
        return self.waveform.get_freq()

    def get_id(self):
        return int(self.num)
