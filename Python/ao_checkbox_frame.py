import tkinter as tk

from checkbox import CheckBox
from converter_and_validator import check_shape


class ChooseAOFrame(tk.Frame):
    def __init__(self, master, shape, indexes, callback):
        """
        :param master: tk master
        :param shape: Shape of AO connections on physical device, 2d tuple like (2,3).
        :type indexes: tuple
        """
        super().__init__(master)

        self._title = tk.Label(self, text='Analog Output', font=("Arial", 14))
        self._title.grid(row=0, column=0, rowspan=1, columnspan=shape[1])

        self._checkboxes = []

        check_shape(shape, indexes, obj_name='Analog Output')
        self._create_widgets(shape, indexes, callback, row=1, column=0)

    def _create_widgets(self, shape, indexes, callback, row, column):
        rows = shape[0]
        cols = shape[1]
        for i in range(rows):
            for j in range(cols):
                index = indexes[cols * i + j]
                checkbox = CheckBox(self, index, command=callback)
                checkbox.grid(row=row+i, column=column+j,sticky='nswe')
                self._checkboxes.append(checkbox)

    def get_available_ao(self):
        """
        :return: a list of indexes of active ao channel
        :rtype: list of int
        """
        available_ao = []

        for checkbox in self._checkboxes:
            is_available = checkbox.var.get()
            if is_available:
                available_ao.append(checkbox.index)

        return available_ao

