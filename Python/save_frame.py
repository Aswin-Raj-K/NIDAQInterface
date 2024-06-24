import tkinter as tk
from tkinter import messagebox

from gui_label_entry_and_strvar import LabelEntryStrVar


class SaveFrame(tk.Frame):
    """
    Frame for file naming and saving
    """
    def __init__(self, master):
        """
        Spawn title/label/entries for save frame
        :param master: master frame/window of this SaveFrame instance
        """
        super().__init__(master, highlightbackground="black", highlightthickness=2)

        self._create_widgets()

    def _create_widgets(self):
        self._title = tk.Label(self, text='File Name', font=("Arial", 14))
        # Create experiment info entries
        self._sample_id = LabelEntryStrVar(master=self, label='Sample ID:', entry_width=20)
        self._device_id = LabelEntryStrVar(master=self, label='Device ID:', entry_width=20)
        self._molecule = LabelEntryStrVar(master=self, label='Molecule:', entry_width=20)
        self._concentration = LabelEntryStrVar(master=self, label='Concentration:', entry_width=20)

        # Trace each variables
        self._sample_id.var.trace('w', self._file_name_changed)
        self._device_id.var.trace('w', self._file_name_changed)
        self._molecule.var.trace('w', self._file_name_changed)
        self._concentration.var.trace('w', self._file_name_changed)

        # Spawn a dynamic label for user to preview name of file
        self.file_name_label = tk.Label(self, text='Filename Prev:')
        self.file_name = tk.Label(self, text='')

        # grid everything
        self._title.grid(row=0, column=0, columnspan=2)
        self.grid_rowconfigure(1, minsize=10)
        self._sample_id.grid(row=2, column=0)
        self.grid_rowconfigure(3, minsize=5)
        self._device_id.grid(row=4, column=0)
        self.grid_rowconfigure(5, minsize=5)
        self._molecule.grid(row=6, column=0)
        self.grid_rowconfigure(7, minsize=5)
        self._concentration.grid(row=8, column=0)
        self.grid_rowconfigure(9, minsize=5)
        self.file_name_label.grid(row=10, column=0)
        self.file_name.grid(row=10, column=1,sticky='nw')
        self.grid_rowconfigure(11, minsize=5)

    def _file_name_changed(self, var, index, mode):
        """
        Callback function activated when user enters/changes experiment information
        """
        # DEMO: don't have a file name for now
        self.file_name['text'] = self.combine_values([self._sample_id.var.get(),self._device_id.var.get(),self._molecule.var.get(),self._concentration.var.get()])

    def get_sample_id(self) -> str:
        sample_id = self._sample_id.var.get()
        return sample_id

    def get_device_id(self):
        device_id = self._device_id.var.get()
        return device_id

    def get_molecule(self):
        molecule = self._molecule.var.get()
        return molecule

    def get_concentration(self):
        concentration = self._concentration.var.get()
        return concentration

    def get_filename(self):
        """
        get filename without wave selection
        :rtype: str
        """
        filename = self.file_name.cget('text')
        return filename.strip()

    def check_empty(self):
        sample_id = self._sample_id.var.get()
        device_id = self._device_id.var.get()
        molecule = self._molecule.var.get()
        concentration = self._concentration.var.get()
        print(sample_id, device_id, molecule, concentration)
        if not (sample_id or device_id or molecule or concentration):
            messagebox.showerror('Ha', 'You forgot to enter experiment info')
            raise ValueError

    def combine_values(self, data):
        # Filter out empty values from the array
        non_empty_values = [value for value in data if value]

        # Join the non-empty values with underscores
        combined_string = "_".join(non_empty_values)

        return combined_string
