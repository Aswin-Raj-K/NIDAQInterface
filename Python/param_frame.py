import tkinter as tk

from gui_label_entry_and_strvar import LabelEntryStrVar


class ParamFrame(tk.Frame):
    """
    A frame for dynamic parameter entry that generates entries and labels according to wave registry
    """
    def __init__(self, master, registry, current_selection):
        """
        Initialize a parameter frame without entries
        :param master: master frame
        :param registry: wave registry
        :param current_selection: current selection in master.ComboBox
        """
        super().__init__(master)
        self._registry = registry

        self.current_selection = current_selection
        self.param_entries = {}

        # keep the row from being occupied
        self._row_updater = 0

    def _new_entry(self, param_name, default, unit):
        """
        spawn a new entry with a label, append the variable
        :param default: default value for that entry
        :param param_name: name of the entry, will appear in label
        :param unit: unit of the parameter
        """
        entry = LabelEntryStrVar(self, label=f'{param_name.replace("_"," ")}:', unit=unit, default_entry=default, )
        self.grid_rowconfigure(self._row_updater, minsize=5)
        entry.grid(row=self._row_updater + 1, column=0, label_sticky='e')
        self.param_entries.update({param_name: entry})

        self._row_updater += 2

    def change_param(self, event):
        """
        This function is called when a selection is made in Combobox.
        :param event: required by tkinter, serves no use in following code.
        """
        # Destroy all param entries (if they exist), clear entry dictionary
        for widgets in self.winfo_children():
            widgets.destroy()
        self.param_entries.clear()
        assert not self.param_entries  # check is dict is empty

        # Update name of wave, Triangular or Nshape or UserDefined or sth else
        wave = self.current_selection.get()
        assert wave in self._registry.keys()

        # extract information from registry
        param_names = self._registry[wave]['params']
        param_defaults = self._registry[wave]['default']
        param_units = self._registry[wave]['unit']

        # Clear row configurations
        for i in range(self.grid_size()[1]):
            self.grid_rowconfigure(i, weight=0, minsize=0)

        # spawn a widget for every param
        for i in range(len(param_names)):
            param = param_names[i]
            default = param_defaults[i]
            unit = param_units[i]
            self._new_entry(param, default, unit)

    def get_params(self) -> dict:
        """
        Get user input of params
        :return param_dict: name:value pair of wavefrom parameters
        """
        param_dict = {}
        for name in self.param_entries.keys():
            value = self.param_entries[name].var.get()
            param_dict.update({name: value})
        return param_dict
