import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

from param_frame import ParamFrame
from converter_and_validator import check_valid_path, convert_to_float


class AOFrame(tk.Frame):
    """
    A frame to collect all user inputs by entry/combobox. It handles input collection and checking input format.
    Use get_* methods to check and fetch user input.
    _check_* methods handles input checking. they Raise error and display error message to user.
    Note: This frame auto grab from registry to generate param_frame.
    """

    def __init__(self, master, index, registry):
        """
        Collect AO specific inputs
        :param master: master frame
        :param name: name thats going to display when channel is created
        :param registry: wave_registry
        :type registry: dict
        """
        super().__init__(master, highlightbackground="black", highlightthickness=2, padx=10, pady=10)
        self._registry = registry

        self._title = tk.Label(self, text=f'AO {index}', font=("Arial", 14))
        self._title.grid(row=0, column=0, columnspan=3)

        self._creat_widgets()

    def _creat_widgets(self):
        self._combobox_label = tk.Label(self, text='Select Waveform:', font=("Arial", 10))

        # Combobox, add selections ('values')
        self.current_selection = tk.StringVar()
        available_wave = list(self._registry.keys())
        self._wave_combobox = ttk.Combobox(self, textvariable=self.current_selection, state='readonly')
        self._wave_combobox['values'] = available_wave

        # Param frame: a slave frame under wave frame for entries. Store registry inside this frame
        self.wave_param_frame = ParamFrame(self, self._registry, self.current_selection)

        # Event handler for Param frame
        # Everytime there is 'Combobox Selection' event, wave_changed() function is called
        self._wave_combobox.bind('<<ComboboxSelected>>', self.wave_param_frame.change_param)

        self._combobox_label.grid(row=40, column=0, sticky='n')
        self._wave_combobox.grid(row=41, column=0, columnspan=3)
        self.wave_param_frame.grid(row=42, column=0, columnspan=3)

    def get_wave_selection(self) -> str:
        """
        Get wave selection in combobox
        :return: Wave Selection
        :rtype: str
        """
        wave_selection = self.current_selection.get()

        # Check for valid input
        self._check_wave_selection(wave_selection)

        return wave_selection

    def get_wave_param(self) -> dict:
        """
        get all user input params as a dictionary of float
        if user input is in the wrong type (float for predetermined wave), display error message and raise TypeError
        """
        param_dict = self.wave_param_frame.get_params()
        param_dict = self._check_and_convert_wave_param(param_dict)

        return param_dict

    def _check_wave_selection(self, wave_selection):
        """
        Interrupt running and pop a error window if wave_selection is not valid.
        """
        if wave_selection not in self._registry:
            messagebox.showerror(message='Please select a Waveform')
            raise ValueError

    def _check_and_convert_wave_param(self, param_dict):
        """
        Check param inputs. For preset wave, try convert to float. For user-defined wave, check if path is valid.
        :return: Two possible returns:
            - for preset wave: {'param_name1': float(value1), 'param_name2': float(value2), ...}
            - for user defined wave: {'path': 'path_str'}
        """
        wave_selection = self.current_selection.get()

        if wave_selection == 'user_wave':
            check_valid_path(param_dict)
        else:
            param_dict = self._convert_wave_param_to_float(param_dict)
        return param_dict

    @staticmethod
    def _convert_wave_param_to_float(param_dict: dict) -> dict:
        """
        :return: A dict of params
        :rtype: float
        """
        for key in param_dict.keys():
            param = param_dict[key]
            param_float = convert_to_float(param, obj_name=key)
            param_dict[key] = param_float
        return param_dict
