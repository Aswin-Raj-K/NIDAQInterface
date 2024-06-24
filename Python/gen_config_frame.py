import tkinter as tk
from gui_label_entry_and_strvar import LabelEntryStrVar
from converter_and_validator import convert_to_int

class GenConfigFrame(tk.Frame):
    """
    A frame to collect all user inputs by entry/combobox. It handles input collection and checking input format.
    Use get_* methods to check and fetch user input.
    _check_* methods handles input checking. they Raise error and display error message to user.
    Note: This frame auto grab from registry to generate param_frame.
    """

    def __init__(self, master):
        """
        Initialize the Channel frame and pack combobox and param frame.
        :param master: master frame
        :param channel_name: name thats going to display when channel is created
        :param registry: wave_registry
        :type registry: dict
        """
        super().__init__(master, highlightbackground="black", highlightthickness=2)
        # Create the inner frame for content
        self._create_widgets()

    def _create_widgets(self):
        self.title = tk.Label(self, text='Config', font=("Arial", 14))
        self.samplingFrequency = LabelEntryStrVar(master=self, label='Sampling Freq:', unit='Hz', default_entry='20000')
        self.sectionTime = LabelEntryStrVar(master=self, label='Recording Batch Time:', unit='min', default_entry='10')
        self.samplesPerChannel = LabelEntryStrVar(master=self, label='Samples Per Channel:', unit='samples', default_entry='20000')

        # Grid everything
        self.title.grid(row=0, column=0, columnspan=3)
        self.grid_rowconfigure(1, minsize=10)
        self.samplingFrequency.grid(row=2, column=0)
        self.grid_rowconfigure(3, minsize=5)
        self.samplesPerChannel.grid(row=4, column=0)
        self.grid_rowconfigure(5, minsize=5)
        self.sectionTime.grid(row=6, column=0)
        self.grid_rowconfigure(7, minsize=5)

    def getSectionTime(self):
        sectionTime = self.sectionTime.var.get()
        return int(sectionTime)

    def getSamplesPerChannel(self):
        samplesPerChannel = self.samplesPerChannel.var.get()
        return int(samplesPerChannel)

    def getSamplingFrequency(self) -> int:
        """
        get user input sample rate in integer
        :return samp_rate_int: sampling rate of wave generation and reading (same value)
        """
        samp_rate = self.samplingFrequency.var.get()
        samp_rate_int = convert_to_int(samp_rate, 'Sample Frequency')
        assert type(samp_rate_int) is int
        return samp_rate_int
