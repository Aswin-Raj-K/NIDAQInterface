import tkinter as tk
from tkinter import ttk

class CtrlFrame(tk.Frame):
    """
    Control Frame is a frame of buttons. Each button has a callback function attached to it.
    """
    def __init__(self, master, start, record, stop, clear, save, add_plotter, remove_plotter):
        super().__init__(master)

        # Create buttons
        self._start_btm = tk.Button(self, text='Start', command=start, width=10)
        self._record_btm = tk.Button(self, text='Record', command=record, width=10)
        self._stop_btm = tk.Button(self, text='Stop', command=stop, width=10)
        self._clear_btm = tk.Button(self, text='Clear', command=clear, width=10)
        self._add_plot_btm = tk.Button(self, text='Add Plot', command=add_plotter, width=10)
        self._remove_plot_btm = tk.Button(self, text='Remove Plot', command=remove_plotter, width=10)
        self._save_btm = tk.Button(self, text='Path', command=save, width=10)
        self._line1 = ttk.Separator(self, orient="horizontal")
        self._line2 = ttk.Separator(self, orient="horizontal")

        # Grid buttons
        self._start_btm.grid(row=0, column=0)
        self._record_btm.grid(row=1, column=0)
        self._stop_btm.grid(row=2, column=0)
        self._clear_btm.grid(row=3, column=0)
        self._line1.grid(row=4, column=0,sticky='ew')
        self._add_plot_btm.grid(row=5, column=0)
        self._remove_plot_btm.grid(row=6, column=0)
        self.grid_rowconfigure(4, minsize=15)
        self._line2.grid(row=7, column=0, sticky='ew')
        self.grid_rowconfigure(7, minsize=15)
        self._save_btm.grid(row=8, column=0)

    def updateAvailableButtons(self, reading, recording, cleared, plotEmpty):
        """
        Enable/Disable buttons based on current status
        :param reading: status boolean
        :param recording: status boolean
        :param cleared: status boolean
        :return: None
        """
        if not reading and not recording and cleared:
            self._start_btm['state'] = 'normal'
        else:
            self._start_btm['state'] = 'disabled'

        if reading and not recording:
            self._record_btm['state'] = 'normal'
        else:
            self._record_btm['state'] = 'disabled'

        if reading:
            self._stop_btm['state'] = 'normal'
        else:
            self._stop_btm['state'] = 'disabled'

        if not reading and not recording and not cleared:
            self._clear_btm['state'] = 'normal'
        else:
            self._clear_btm['state'] = 'disabled'

        if not reading and not recording:
            self._save_btm['state'] = 'normal'
        else:
            self._save_btm['state'] = 'disabled'

        if not reading and not recording and cleared:
            self._add_plot_btm['state'] = 'normal'
            if not plotEmpty:
                self._remove_plot_btm['state'] = 'normal'
            else:
                self._remove_plot_btm['state'] = 'disabled'
        else:
            self._add_plot_btm['state'] = 'disabled'


    def setFolderPath(self, folderPath):
        if not hasattr(self, 'path'):
            self.path = tk.Label(self, text=f'Path: {folderPath}', font=("Arial", 10))
        else:
            self.path.config(text=f'Path: {folderPath}')

        self.path.grid(row=9, column=0)

