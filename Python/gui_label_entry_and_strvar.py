import tkinter as tk


class LabelEntryStrVar:
    """
    A container of 3 widgets: a string var, a label, and an entry. The code exist to reduce redundancy
    """
    def __init__(self, master, label, unit=None, default_entry=None, entry_width=10, entry_state='normal'):
        self.var = tk.StringVar(value=default_entry)
        self.label = tk.Label(master, text=label)
        self.entry = tk.Entry(master, textvariable=self.var, width=entry_width, state=entry_state)
        self.unit = tk.Label(master, text=unit)

    def grid(self, row, column, label_sticky='W'):
        self.label.grid(row=row, column=column, sticky=label_sticky)
        self.entry.grid(row=row, column=column + 1)
        self.unit.grid(row=row, column=column + 2)
