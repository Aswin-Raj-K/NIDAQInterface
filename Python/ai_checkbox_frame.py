import tkinter as tk

from checkbox import CheckBox
from converter_and_validator import check_shape


class ChooseAIFrame(tk.Frame):
    def __init__(self, master, shape, indexes, callback):
        """
        :param master: tk master
        :param shape: Shape of AI connection array on physical device, 2d tuple like (2,3).
        :param callback: Function for updating available AIs, it is bound to change in checkbox
        :type indexes: tuple
        """
        super().__init__(master)

        self._title = tk.Label(self, text='Analog Input', font=("Arial", 14))
        self._title.grid(row=0, column=0, rowspan=1, columnspan=shape[1])

        self._checkboxes = []

        check_shape(shape, indexes, obj_name='Analog Input')
        self._create_widgets(shape, indexes, callback, row=1, column=0)

    def _create_widgets(self, shape, indexes, callback, row, column):
        rows = shape[0]
        cols = shape[1]

        for i in range(rows):
            for j in range(cols):
                index = indexes[cols * i + j]
                checkbox = CheckBox(self, index, command=callback)
                checkbox.grid(row=row+i, column=column+j)
                self._checkboxes.append(checkbox)
        
        # command here only acts as a place holder
        self.show_graph = CheckBox(self, index='Show Input Graph', command=callback)
        self.show_graph.grid(row=row+rows+1, column=0, columnspan=cols)

    def get_available_ai(self):
        """
        Get all selected AI
        :return: Indexes of All selected AI
        :rtype: list of int
        """
        available_ai = []

        for checkbox in self._checkboxes:
            is_available = checkbox.var.get()
            if is_available:
                available_ai.append(checkbox.index)

        return available_ai

    def get_show_graph(self) -> bool:
        """
        :return: if to show AI vs t graph
        """
        # turn a IntVar (0 or 1) into Bool
        return bool(self.show_graph.var.get())
