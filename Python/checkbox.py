import tkinter as tk


class CheckBox:
    def __init__(self, master, index, command):
        self.index = index
        self.var = tk.IntVar()
        self.checkbox = tk.Checkbutton(master, variable=self.var, onvalue=1, offvalue=0, command=command, text=f'{index}')

    def grid(self, row, column, rowspan=1, columnspan=1, sticky = 'nw'):
        self.checkbox.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
