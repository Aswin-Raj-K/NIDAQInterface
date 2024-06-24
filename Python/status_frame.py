import tkinter as tk

from gui_stopwatch_frame import StopwatchFrame


class StatusFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()

    def _create_widgets(self):
        self._status = tk.Label(self, text='Standby', fg='green4', font=('Helvetica', 20))
        self.stopwatch = StopwatchFrame(self)

        self._status.grid(row=0, column=0)
        self.stopwatch.grid(row=1, column=0)

    def update_status(self, reading, recording, cleared):
        if reading and not recording:
            self._status['text'] = 'Reading...'
            self._status.config(fg="Orange")
        elif reading and recording:
            self.stopwatch.start()
            self._status['text'] = 'Recording...'
            self._status.config(fg="Blue")
        elif not reading and not recording and not cleared:
            self.stopwatch.pause()
            self._status['text'] = 'Stopped'
            self._status.config(fg="Red")
        elif not reading and cleared:
            self.stopwatch.reset_time()
            self._status['text'] = 'Standby'
            self._status.config(fg="Green")



