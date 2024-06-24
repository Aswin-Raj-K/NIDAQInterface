import tkinter as tk


# This program is designed to count up from zero
class StopwatchFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgtes()
        self.running = False
        self.timer = [0, 0, 0]  # [minutes ,seconds, centiseconds]
        self.timeString = str(self.timer[0]) + ':' + str(self.timer[1]) + ':' + str(self.timer[2])
        self.update_time()

    def _create_widgtes(self):
        self.timeFrame = tk.LabelFrame(self, text='Time Passed')
        self.timeFrame.grid(row=0, column=0, sticky='W')

        self.show = tk.Label(self.timeFrame, text='00:00:00', font=('Helvetica', 30))
        self.show.grid(row=0, column=0)


    def update_time(self):
        if self.running == True:  # Clock is running
            self.timer[2] += 1  # Count Down

            if self.timer[2] >= 60:  # 100 centiseconds --> 1 second
                self.timer[2] = 0  # reset to zero centiseconds
                self.timer[1] += 1  # add 1 second

            if self.timer[1] >= 60:  # 60 seconds --> 1 minute
                self.timer[0] += 1  # add 1 minute
                self.timer[1] = 0  # reset to 0 seconds

            self.timeString = "{:02d}".format(self.timer[0]) + ':' + "{:02d}".format(self.timer[1]) + ':' + "{:02d}".format(self.timer[2])
            self.show.config(text=self.timeString)
        self.after(1000, self.update_time)

    def start(self):  # Start the clock
        self.running = True
        print('Clock Running...')

    def pause(self):  # Pause the clock
        self.running = False
        print('Clock Paused')

    def reset_time(self):  # Reset the clock
        self.running = False
        self.timer = [0, 0, 0]
        print('Clock is Reset')
        self.show.config(text='00:00:00')
