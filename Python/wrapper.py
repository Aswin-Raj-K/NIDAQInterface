import time
import nidaqmx
from nidaqmx.constants import * #(AcquisitionType)
from nidaqmx.stream_readers import (
    AnalogMultiChannelReader)
from nidaqmx.stream_writers import (
    AnalogMultiChannelWriter,CounterWriter)
import numpy as np
from values import DEBUGGING
#from triangle_wave import *
#from user_wave import *

class AnalogInStream(nidaqmx.Task):
    def __init__(self, device, channels, nr_samples):
        nidaqmx.Task.__init__(self)
        if not DEBUGGING:
            for ch in channels:                      #device.name
                self.ai_channels.add_ai_voltage_chan("Dev1" + "/ai"+str(ch))
            self.reader = AnalogMultiChannelReader(self.in_stream)

        self.nr_channels = len(channels)
        self.nr_samples = int(nr_samples)

        self.acq_data = np.zeros((self.nr_channels, self.nr_samples), dtype = np.float64)


    def configure_clock(self, sample_rate, device):
        try:
            self.timing.cfg_samp_clk_timing(int(sample_rate), sample_mode= AcquisitionType.CONTINUOUS, source='/'+"Dev1"+'/ao/SampleClock',samps_per_chan=self.nr_samples*50)
        except NameError:                                       
            pass

    def acquire_data(self):
        if hasattr(self, 'time1'):
            print("Total Time:", time.time() - self.time1)
            print("=====================")
        self.time1 = time.time()
        if not DEBUGGING:
            self.reader.read_many_sample(self.acq_data, number_of_samples_per_channel=self.nr_samples)
        else:
            time.sleep(0.5)
            self.acq_data = np.random.rand(self.nr_channels, self.nr_samples)

        time2=time.time()
        print("Nidaq Time: ", time2-self.time1)

class AnalogOutStream(nidaqmx.Task):
    def __init__(self, device, channels, nr_samples):
        nidaqmx.Task.__init__(self)
        if not DEBUGGING:
            for ch in channels:                         #"Dev1/ao0"/device.name
                self.ao_channels.add_ao_voltage_chan("Dev1"+"/ao"+str(ch))
            self.writer = AnalogMultiChannelWriter(self.out_stream)#AnalogSingleChannelWriter(self.out_stream)

        self.nr_channels = len(channels)
        self.nr_samples = int(nr_samples)



        self.write_data = np.zeros((self.nr_samples, self.nr_channels))

        self.change_flag = True

    def configure_clock(self, sample_rate):
        self.timing.cfg_samp_clk_timing(int(sample_rate), sample_mode= AcquisitionType.CONTINUOUS, samps_per_chan=self.nr_samples*50)

    def update_data(self, data):
        self.write_data = data
        self.change_flag = True

    def perform_write(self):
        if self.change_flag:
            if not DEBUGGING:
                self.writer.write_many_sample(self.write_data)
            self.change_flag = False
        if not DEBUGGING:
            self.start()

if __name__ == "__main__":
    with nidaqmx.Task() as task:
        task.co_channels.add_co_pulse_chan_time(counter = "Dev2/ao1")
        task.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS)
        cw = CounterWriter(task.out_stream, True)
        task.start()
        cw.write_one_sample_pulse_frequency(100, 0.1, 10)
    
    sample_rate = 2000
    print(f'sample rate = {sample_rate/1e6:.1f} MHz')


    
