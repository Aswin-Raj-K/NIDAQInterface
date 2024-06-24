import threading
import tkinter as tk
from tkinter import Scrollbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np
import time as tm


class Plotter(tk.Toplevel):
	def __init__(self, master, totalChannels, noOfSamplingPoints, names=[], labelRounding=2):
		super().__init__(master)
		self.root = self
		self.totalChannels = totalChannels
		self.noOfSamplingPoints = noOfSamplingPoints
		self.names = names
		self.labelRounding = labelRounding
		self.protocol("WM_DELETE_WINDOW", self.on_closing)

		label = tk.Label(self.root, text="Channel Plots", pady=5, font=("Arial", 16))
		label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		# Make Plot Space in TK
		# Calculate the number of rows and columns for subplot arrangement
		num_cols = 2
		num_rows = math.ceil(totalChannels / num_cols)

		# Calculate the figure size based on the number of subplots
		figsize_x = 8 * num_cols
		figsize_y = 4 * num_rows
		self.fig = Figure(figsize=(2 * figsize_y, figsize_y), dpi=100)  # Adjusted figure size
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
		self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		rows = math.ceil(totalChannels / 2)

		self.graphList = []
		for i in range(totalChannels):
			self.graphList.append(self.fig.add_subplot(rows, 2, i + 1))

		self.fig.subplots_adjust(wspace=0.5, hspace=0.8)  # Adjusted spacing
		self.x_values = []
		self.y_values = []

		label = tk.Label(self.root, text="Sampling points", pady=5, font=("Arial", 16))
		label.pack(side=tk.TOP)

		# Create a container frame to hold all the frames
		labelContainer = tk.Frame(self.root)
		labelContainer.pack(side=tk.TOP, anchor='center')

		# Add labels below each plot based on samplingPoints
		self.labels = []
		for i, rows in enumerate(noOfSamplingPoints):
			frame = tk.Frame(labelContainer)
			frame.pack(side=tk.LEFT, anchor='n', padx=10, expand=True, fill=tk.BOTH)
			if self.names:
				label = tk.Label(frame, text=self.names[i], pady=5, font=("Arial", 10), width=10, anchor='nw')
			else:
				label = tk.Label(frame, text=f'Plot {i}', pady=5, font=("Arial", 10), width=10, anchor='nw')
			label.pack(side=tk.TOP, anchor='n')
			for j in range(rows):
				label = tk.Label(frame, text="", pady=5, font=("Arial", 10), width=10, anchor='nw')
				label.pack(side=tk.TOP, anchor='n')
				self.labels.append(label)

	def updatePlot(self, time, readData, custom_x, custom_y, gain):
		self.x_values = time
		self.y_values = readData
		for j, i in enumerate(self.graphList):
			i.clear()
			x = self.y_values[custom_x[j]]
			y = self.y_values[custom_y[j]]/gain[j] * 1e9
			i.plot(x, y, color='r', markersize=0.5)
			i.grid(True)
			i.set_ylabel("Current (nA)", fontsize=8)
			i.set_xlabel("Voltage (V)", fontsize=8)
			if self.names:
				i.set_title(self.names[j], fontsize=12)
			else:
				i.set_title(f'Plot {j}', fontsize=12)
		time1 = tm.time()
		self.updateUI()
		time2 = tm.time()
		print("UpdateUI:",time2-time1)

	def updateUI(self):
		self.canvas.draw()
		self.root.update()



	def updateSamplingPoints(self, data):
		m = 0
		if self.labels is not None:
			for n, i in enumerate(self.noOfSamplingPoints):
				for j in range(i):
					if data[n][j] is not None:
						self.labels[m].config(text=f"V{j + 1}: {round(data[n][j], self.labelRounding)}")
					else:
						self.labels[m].config(text=f"V{j + 1}: -")
					m += 1
	def on_closing(self):
		pass

