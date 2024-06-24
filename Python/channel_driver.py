import threading
import time

import nidaqmx as dq
import numpy as np

from plotter import *
from tkinter import messagebox, filedialog
import csv
from math import gcd

# from n_wave import *
from read_channel import *
from write_channel import *
from triangle_wave import *
from wrapper import *

class Channel_Driver:
	def __init__(self, root, num, sample_rate, device_name='Dev1', show_graphs=False):
		self.root = root
		self.write_rate = int(sample_rate)  # write and sample rate should be equal
		self.sample_rate = int(sample_rate)
		self.time_len = 60 * 60 * 5
		self.time = []
		self.voltages = []  # [[],[],[],[]]
		self.current_values = np.array([])
		self.show_graphs = show_graphs
		self.device_name = device_name

		self.xChannels = []
		self.yChannels = []
		self.gain = []
		self.point_plots = []
		self.point_plots_count = []
		self.tts = []

		self.readChannels = []  # x for x in range(2*num)]
		self.write_channels = []  # x for x in range(num)]
		self.isRecording = False
		self.yHolder = []
		self.timeHolder = []
		self.writeThreadRunning = False


	def start(self):

		dev = dq.system.Device(name=self.device_name)
		self.ao = AnalogOutStream(dev, self.write_channels, self.write_rate)
		self.ai = AnalogInStream(dev, self.readChannels, self.sample_rate)

		if not DEBUGGING:
			self.ai.configure_clock(self.sample_rate, self.ao.devices[0])  # sample_rate
			self.ao.configure_clock(self.write_rate)

		self.ao.update_data(self.waveforms)
		self.ao.perform_write()

		if not DEBUGGING:
			self.ai.start()

		# plotThread = threading.Thread(target=self.showPlot)
		# plotThread.start()
		self.showPlot()

	def showPlot(self):

		self.plot = Plotter(self.root, len(self.xChannels),self.point_plots_count)
		if not self.xChannels:
			self.plot.withdraw()

		readThread = threading.Thread(target=self.run)
		readThread.daemon = True
		readThread.start()
		# self.plot.root.mainloop()

	def run(self):
		length_voltages = len(self.voltages)
		self.pausePoint = 0
		time_step = (1 / self.sample_rate)

		start_time = 0.0
		internal_start_time = time.time()

		Fc = 10e3
		N = self.sample_rate / (2 * Fc)
		samplesPerChannel = self.root.getSamplesPerChannel()
		while time.time() - internal_start_time < self.time_len:
			self.timeHolder = self.time[self.pausePoint:self.pausePoint + samplesPerChannel]
			# y_holder = [self.smoothData(ls[self.pause_point:len(self.time_x)],N) for ls in self.voltages]
			# self.yHolder = [ls[self.pausePoint:len(self.time)] for ls in self.voltages]
			self.yHolder = [i[0:samplesPerChannel] for i in self.ai.acq_data]

			time1 = time.time()
			if not self.writeThreadRunning:
				self.plot.updatePlot(self.timeHolder[:], self.yHolder[:], self.xChannels, self.yChannels, self.gain)
			time2 = time.time()
			print("Update Plot : ", time2-time1)


			if not self.writeThreadRunning:
				time1 = time.time()
				samp = []
				print(self.xChannels)
				for k, i in enumerate(self.yChannels):
					m = []
					for n, j in enumerate(self.point_plots[k]):
						su,sd = self.findSamplingPoint(self.yHolder[i],j,1/self.sample_rate)
						m.append(self.yHolder[self.xChannels[k]][sd]/self.gain[k] if sd is not None and n > 1 else self.yHolder[self.xChannels[k]][su]/self.gain[k] if su is not None and n <= 1 else None)

					samp.append(m)
				print(samp)
				self.plot.updateSamplingPoints(samp)
				time2 = time.time()
				print("Update label : ", time2-time1)



			if not self.isRecording:
				self.time = []
				self.voltages = [[] for _ in range(length_voltages)]
				self.pausePoint = 0
			else:
				self.pausePoint += self.write_rate

			self.ai.acquire_data()

			if len(self.time) > 0:
				next_time = self.time[-1] + time_step
			else:
				next_time = start_time

			self.addDataPoint(self.ai.acq_data, next_time, time_step, start_time)

		self.ao.stop()
		self.ao.update_data(np.array([np.array([0.0 for x in range(len(self.waveforms[0]))]) for y in range(len(self.waveforms))]))
		self.ao.perform_write()
		self.ao.stop()
		self.isRecording = False
		self.ai.stop()
		self.ai.close()
		self.ao.close()

	def add_writer(self, channels):
		# self.waveforms = np.array([x.get_array() for x in channels])
		self.write_channels = [x.get_id() for x in channels]

		#############
		full_waves = []
		hold_waves = []
		wave_freqs = [int(x.get_freq()) for x in channels]
		# print(wave_freqs)
		wave_lens = [len(x.get_array()) for x in channels]
		new_lens = []
		gcf = wave_freqs[0]
		for i in wave_freqs[1:]:
			gcf = gcd(gcf, i)
		for j in range(len(wave_freqs)):
			freq = wave_freqs[j]
			old_len = wave_lens[j]
			new_lens.append(int(freq / gcf) * old_len)
			holder = np.array([])
			for k in range(int(freq / gcf)):
				holder = np.append(holder, channels[j].get_array())
			hold_waves.append(holder)
		print(hold_waves)
		max_len = max(new_lens)
		for wave in hold_waves:
			complete_wave = np.append(wave, np.array([wave[-1] for x in range(max_len - len(wave))]))
			full_waves.append(complete_wave)
		self.waveforms = np.array(full_waves)

	def add_readers(self, channels):
		self.readChannels = [x.get_id() for x in channels]
		self.reader_names = [x.get_name() for x in channels]
		self.voltages = [[] for x in channels]
		self.time_shown = [x.get_time_shown() for x in channels]

	def add_custom(self, custom):
		# print(custom)
		self.trig_results = []
		self.xChannels = []
		self.yChannels = []
		self.gain = []
		self.custom_names = [x for x in custom]
		self.point_plots_count = []
		self.point_plots = []
		for key in custom:
			x = int(custom[key]['x'])
			y = int(custom[key]['y'])
			if x in self.readChannels:
				self.xChannels.append(self.readChannels.index(x))
				self.trig_results.append([])
			else:
				raise Exception("Custom Graph: channel {} is missing.".format(x))
			if y in self.readChannels:
				self.yChannels.append(self.readChannels.index(y))
			else:
				raise Exception("Custom Graph: channel {} is missing.".format(y))
			self.gain.append(int(custom[key]['gain']))
			samp = custom[key]['sampling_time']
			self.point_plots.append(samp)
			self.point_plots_count.append(len(samp))

	def record(self):
		self.isRecording = True

	def addDataPoint(self, volts, prev_time, time_step, start):  # inputs must be int or float
		time1 = time.time()
		if len(self.readChannels) > 0:
			if len(self.voltages[0]) > self.sample_rate * 60 * self.root.getSectionTime():
				self.clearData()


		self.time.extend([prev_time + (x * time_step) for x in range(len(volts[0]))])
		for i in range(len(self.readChannels)):
			self.voltages[i].extend(volts[i])
		time2 = time.time()
		print("Add Data Point: ", time2-time1)

	def clearData(self):
		if self.isRecording:
			self.writeThreadRunning = True
			writeThread = threading.Thread(target=self.writeData, args=(self.time[:], self.voltages[:]))
			writeThread.daemon = True
			writeThread.start()

		self.pausePoint = 0
		self.voltages = []
		self.time = []
		for i in range(len(self.readChannels)):
			self.voltages.append([])
		print("Data Cleared")

	def writeData(self, time, voltages):
		data = self.getData(time, voltages)
		self.overflowCallBack(data)

	def addOverflowCallBack(self, callback):
		self.overflowCallBack = callback

	def export_data(self):  # tdms
		file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
		if file_path:
			try:
				with open(file_path, 'w', newline='') as file:
					# for column in range((self.time_x//1000000)+1):
					writer = csv.writer(file)
					writer.writerow(['Time (s)', 'Voltage Input', 'Voltage Output'])
					writer.writerows(zip(self.time, self.voltages[0]))
					print(len(self.voltages[0]))
				messagebox.showinfo("Export Successful", "Data exported to CSV file successfully.")
			except Exception as e:
				messagebox.showerror("Export Failed", f"Error occurred while exporting data:\n{str(e)}")

	def get_data(self):
		total_data = {}
		total_data["Time"] = self.time
		i = 0
		for channel in self.voltages:
			total_data[self.reader_names[i]] = channel
			i += 1
		j = 0
		for custom_name in self.custom_names:
			total_data[custom_name + "Gain:{}".format(self.gain[j])] = list(
				np.array(self.voltages[int(self.yChannels[j])]) * (1 / self.gain[j]))
			j += 1
		return total_data

	def getData(self, time, voltages):
		totalData = {}
		totalData["Time"] = time
		i = 0
		for channel in voltages:
			totalData[self.reader_names[i]] = channel
			i += 1
		j = 0
		for custom_name in self.custom_names:
			totalData[custom_name + "Gain:{}".format(self.gain[j])] = list(
				np.array(voltages[int(self.yChannels[j])]) * (1 / self.gain[j]))
			j += 1
		return totalData

	def stop(self):  # Must be used to display after plotting is done     ## NOT A PAUSE AND NOT A MANUAL STOP ##
		self.time_len = 0

	# self.plot.stop_plot()

	def smoothData(self, data, window_size):
		smoothed_data = []
		for i in range(len(data)):
			start = int(max(0, i - window_size // 2))
			end = int(min(len(data), i + window_size // 2 + 1))
			smoothed_value = sum(data[start:end]) / (end - start)
			smoothed_data.append(smoothed_value)
		return smoothed_data

	def findSamplingPoint(self, array1, value, threshold=1e-5, range = 20):
		abs_diff = np.abs(array1 - value)
		within_threshold_indices = np.where(abs_diff < threshold)[0]

		closest_index_up = None
		closest_index_down = None

		for index in within_threshold_indices:
			if np.average(array1[index+1:index+range]) > value and np.average(array1[index-range:index-1]) < value :
				if closest_index_up is None or array1[index] < array1[closest_index_up]:
					closest_index_up = index
			elif np.average(array1[index+1:index + range]) < array1[index] and np.average(array1[index - range:index-1]) > array1[index] :
				if closest_index_down is None:
					closest_index_down = index
				elif abs(array1[closest_index_down]-value) > abs(array1[index]-value):
					closest_index_down = index
		return closest_index_up, closest_index_down


if __name__ == "__main__":
	samples = TriangleWave(-0.4, 1.3, 400, 20000, 60)
	samples2 = TriangleWave(2, 3, 800, 20000, 60)
	# samples2= NWave(-0.2,0.6,-0.02,200,20000,10)
	# samples4= UserWave("src/User_Test.txt", 20000)

	# (name,      sample rate, total time length, resistance)
	test = Channel_Driver(1, 20000)  # , samples2, 5500000)
	ai0 = Reader(0, "reader 0", 0.25)
	ai1 = Reader(1, "reader 1", 0.25)
	ao0 = Writer(0, "writer 0", samples)
	ao1 = Writer(1, "writer 1", samples2)
	# ao0 = Writer(0, "writer 2", samples)
	# ao1 = Writer(1, "writer 3", samples2)
	test.add_readers([ai0, ai1])
	test.add_writer([ao0, ao1])
	test.add_custom({'graph1': {'x': '0', 'y': '1', 'gain': 1000000, 'sampling_time': [4]},
					 'graph2': {'x': '0', 'y': '1', 'gain': 1000000, 'sampling_time': [0]}})
	test.start()
	test.export_data()
# print(test.get_data().items())

