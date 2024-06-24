import tkinter as tk
from tkinter import ttk

from converter_and_validator import convert_to_float


class PlotFrame(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master,highlightbackground="black", highlightthickness=2, pady=5,padx=5)
        self._name = name
        self._gain_var = tk.StringVar()
        self._gain_var.set('6500000')
        self.plot_volt_container = []

        self._create_widgets(name)

    def _create_widgets(self, name):
        self._title = tk.Label(self, text=name, font=("Arial", 14), anchor='center')
        self._div = tk.Label(self, text='/')
        self._y_label = tk.Label(self, text='Y: ')
        self._x_label = tk.Label(self, text='X: ')
        self._plot_volt_title = tk.Label(self, text='Sampling Points', font=("Arial", 14))

        self._y_combobox = ttk.Combobox(self, state="readonly", width=4)
        self._x_combobox = ttk.Combobox(self, state="readonly", width=4)
        self._gain_entry = tk.Entry(self, textvariable=self._gain_var, width=7)

        self._add_plot_volt_button = tk.Button(self, text='+', command=self._create_plot_volt)
        self._del_plot_volt_button = tk.Button(self, text='-', command=self._del_plot_volt)

        self._title.grid(row=0, column=0, columnspan=4)
        self.rowconfigure(2,minsize=5)
        self._y_label.grid(row=3, column=0)
        self.grid_rowconfigure(4,minsize=5)
        self._y_combobox.grid(row=3, column=1)
        self._div.grid(row=3, column=2)
        self._gain_entry.grid(row=3, column=3)
        self._x_label.grid(row=5, column=0)
        self._x_combobox.grid(row=5, column=1)
        self._plot_volt_title.grid(row=6, column=0, columnspan=4, pady=(10, 10), sticky='W')
        self._add_plot_volt_button.grid(row=7, column=1, sticky='e', padx=0, pady=(0, 10))
        self._del_plot_volt_button.grid(row=7, column=2, sticky='w', padx=0, pady=(0, 10))
        # self._del_plot_volt_button['state'] = 'disabled'
        self._create_plot_volt(-0.1)
        self._create_plot_volt(0.5)
        self._create_plot_volt(0.6)
        self._create_plot_volt(0.5)
    def update_available_ai(self, available_ai):
        """
        :param available_ai: indexes of available ai
        :type available_ai: list of int
        :return:
        """
        ai_list = [f'{index}' for index in available_ai]
        self._y_combobox['values'] = ai_list
        self._x_combobox['values'] = ai_list

    def get_plot_config(self) -> dict:
        """
        get ploting configuration as a dictionary. an example looks like this:
        graph_dict = {'graph1': {'x': 'ai4', 'y': 'ai2', 'gain': 1000, 'sampling_time': [11, 22, 33, 33]}}
        :return: 
        """
        gain_entry = self._gain_var.get()
        gain = convert_to_float(gain_entry, obj_name=f'Gain for {self._name}')
        assert gain != 0
        x_ai = self._x_combobox.get()
        y_ai = self._y_combobox.get()
        sampling_volt = self.get_plotting_time()
        
        config = {f'{self._name}': {'x': x_ai, 'y': y_ai, 'gain': gain, 'sampling_time': sampling_volt}}
        return config

    def get_plotting_time(self) -> list:
        """
        get all plotting voltage as a list of numbers
        :return: a list of voltages for plotter
        :rtype: list
        """
        time_list = []

        # for each StrVar, try to get value and change it to float. except: raise type error
        for voltage_obj in self.plot_volt_container:
            time = voltage_obj[0].get()
            time_in_float = convert_to_float(time, obj_name='Plotting time')

            time_list.append(time_in_float)

        return time_list

    def _create_plot_volt(self,defaultEntry = None):
        """
        add [var, label, and entry] to plot_volt_list and grid the label and entry
        """
        i = len(self.plot_volt_container) + 1
        var = tk.StringVar(value=defaultEntry)
        label = tk.Label(self, text=f'Plotting V{i}: ')
        entry = tk.Entry(self, textvariable=var, width=6)
        label.grid(row=62 + i, column=0, columnspan=2, pady=(0,5))
        entry.grid(row=62 + i, column=2, columnspan=2,pady=(0,5))
        self.plot_volt_container.append([var, label, entry])
        self._del_plot_volt_button['state'] = 'normal'

    def _del_plot_volt(self):
        """
        delete the last plot_volt entry & label
        """
        if self.plot_volt_container:
            last = self.plot_volt_container[-1]
            last[1].destroy()
            last[2].destroy()
            del last[0]
            self.plot_volt_container.pop(-1)
            if not self.plot_volt_container:
                self._del_plot_volt_button['state'] = 'disabled'


