import os
import threading
import time
import time as tm
import tkinter as tk
from tkinter.messagebox import askyesno
from tkinter import messagebox
from tkinter import filedialog

import nidaqmx
import nptdms
from nptdms import RootObject, GroupObject, ChannelObject, TdmsWriter
import datetime
import copy

from ctrl_frame import CtrlFrame
from ai_checkbox_frame import ChooseAIFrame
from ao_checkbox_frame import ChooseAOFrame
from gen_config_frame import GenConfigFrame
from ao_frame import AOFrame
from save_frame import SaveFrame
from plot_frame import PlotFrame
from status_frame import StatusFrame
from registries import wave_registry, device_registry, savepath
from wave_factory import WaveFactory
from channel_driver import Channel_Driver
from write_channel import Writer
from read_channel import Reader
from n_wave import NWave #DM new
from triangle_wave import TriangleWave #DM new
from values import DEFAULT_FILE_PATH
class MainApplication(tk.Frame):

    """
    This is the main frame for GUI. It is where all other frames resides.
    Main app has access to all frames and is responsible for collecting data and pass them to channel_driver.

    Currently, Channel_driver is an attribute of MainApplication. The controller methods ( self._clicked_*() ) controls
    the drivers and collect data from all frames. They are bind to buttons in CtrlFrame.
    """

    def __init__(self, master):
        super().__init__(master, padx=10, pady=10)

        '''These booleans are safety features to prevent user from not following control procedures, they are set to 
        private to prevent other code from changing it.'''
        # Status boolean. If True, indicates that the program is reading (and plotting)
        self._is_reading = False
        # Status boolean. If True, indicates that the program is recording data (data stored in each channel_driver obj)
        self._is_recording = False
        # Status boolean. If True, indicates that program cache is cleared and a new start can begin
        self._is_cleared = True

        self.plotEmpty = True

        # Container for AO frame: Dict pairs of index:frame_object
        self._ao_frame_container = {}
        # Container for plot frame: List of plotter
        self._plot_frame_container = []
        # Container for saving related info: Dict pairs of 'info_name': info
        self._save_info_container = {}

        self._create_widgets()
        self.update_available_buttons()
        self.filePath = DEFAULT_FILE_PATH
        self.ao_container_frame = None
        self.plot_frame_container = None
    def _create_widgets(self):
        """
        Create and grid frames that resides in main_app.
        """
        # Create all Frames!
        self._ctrl = CtrlFrame(self, start=self._clicked_start, record=self._clicked_record,
                               stop=self._clicked_stop, clear=self._clicked_clear, save=self._clicked_path,
                               add_plotter=self._clicked_add_plotter, remove_plotter=self._clicked_remove_plotter
                               )    # callback func passed into control frame to bind with its buttons
        ai_shape = device_registry['ai']['shape']
        ai_indexes = device_registry['ai']['indexes']
        self._ai_checkbox = ChooseAIFrame(self, ai_shape, ai_indexes, self.update_available_ai)
        ao_shape = device_registry['ao']['shape']
        ao_indexes = device_registry['ao']['indexes']
        self._ao_checkbox = ChooseAOFrame(self, ao_shape, ao_indexes, self.update_available_ao)
        self._save = SaveFrame(self)
        self._gen_config = GenConfigFrame(self)
        self._status = StatusFrame(self)
#         self._nwave = NWave(self) #DM new
#         self._twave = TriangleWave(self) #DMnew

        # Grid everything!
        self._ctrl.grid(row=0, column=0, pady=(0, 10),padx=25)
        self._status.grid(row=0, column=1, sticky='n',padx=25)
        self._ai_checkbox.grid(row=0, column=2, sticky='nw',padx=25)
        self._ao_checkbox.grid(row=0, column=3, sticky='nw',padx=25)
        self._save.grid(row=0, column=4, padx=(10, 10),sticky='nw')
        self._gen_config.grid(row=1, column=0, rowspan=2, padx=(10,0), sticky='nw')

    def update_available_buttons(self):
        """
        Updates CtrlFrame buttons (normal/disables) by status booleans
        :return: None
        """
        is_read = copy.copy(self._is_reading)
        is_roc = copy.copy(self._is_recording)
        is_clr = copy.copy(self._is_cleared)
        plotEmpty = copy.copy(self.plotEmpty)
        self._ctrl.updateAvailableButtons(is_read, is_roc, is_clr, plotEmpty)

    def update_available_ai(self):
        """
        Updates PlotFrame combobox by selection in AICheckboxFrame
        :return: None
        """
        # let plotters know selections have changed
        available_ai = self._ai_checkbox.get_available_ai()
        for plot in self._plot_frame_container:
            plot.update_available_ai(available_ai)

    def update_available_ao(self):
        """
        Update AOFrames by selection made in AO Checkbox Frame.
        """
        available_ao = self._ao_checkbox.get_available_ao()

        if self.ao_container_frame is None:
            self.ao_container_frame = tk.Frame(self)
            self.ao_container_frame.grid(row=1, column=1,columnspan=7, sticky='nw')

        # Destroy unwanted frame
        to_be_del = []
        for index in self._ao_frame_container.keys():
            if index not in available_ao:
                frame = self._ao_frame_container[index]
                frame.destroy()
                to_be_del.append(index)

        # Delete from container
        for index in to_be_del:
            del self._ao_frame_container[index]

        if not available_ao:
            self.ao_container_frame.destroy()
            self.ao_container_frame = None

        # Add new frame
        for index in available_ao:
            if index not in self._ao_frame_container.keys():
                ao_frame = AOFrame(self.ao_container_frame, index, wave_registry)
                self._ao_frame_container.update({index: ao_frame})

        # re-grid
        # next_empty_col = 1
        for index in available_ao:
            # self._ao_frame_container[index].grid(row=1, column=next_empty_col, sticky='nw', padx = 10, pady = (0, 10))
            self._ao_frame_container[index].pack(side='left',padx=(10,0),pady=(0,10), anchor='nw')
            # next_empty_col += 1

    def update_status_frame(self):
        """
        Update StatusFrame by status boolean. This function should always be called after status is changed.
        :return: None
        """
        # make a copy to prevent changing original object
        is_reading = copy.copy(self._is_reading)
        is_recording = copy.copy(self._is_recording)
        is_cleared = copy.copy(self._is_cleared)
        # calls update method of status frame
        self._status.update_status(is_reading, is_recording, is_cleared)

    def _clicked_start(self):
        """
        Start reading and plotting for all channels. This class method fetch data from GUI, instantiates driver, and
        tell driver to start reading and plotting.
        """
        # Prepare for start
        self._check_input()
        assert self._ao_frame_container  # assert not empty
        device_name = device_registry['name']

        # if not self.is_nidaq_connected(device_name):
        #     messagebox.showerror('Hm', 'NIDAQ Not Connected')
        #     return 0


        # Get data
        samp_freq = self._gen_config.getSamplingFrequency()
        available_ai = self._ai_checkbox.get_available_ai()
        show_graph = self._ai_checkbox.get_show_graph()

        # Create driver
        self.driver = self._create_driver(samp_freq, ao_frames=self._ao_frame_container, available_ai=available_ai,
                                          plot_frames=self._plot_frame_container, show_graph=show_graph,
                                          device_name=device_name)

        # Update status
        self._is_reading = True
        self._is_cleared = False
        self.update_available_buttons()
        self.update_status_frame()

        # Start Driver
        self.driver.start()

    def _clicked_record(self):
        self.fileName = self._save.get_filename()
        self.fileName += self.get_waveforms_in_str(self.get_waveforms()) + "_"
        self.folderName = self.fileName + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Start if not already
        if not self._is_reading:
            self._clicked_start()

        # Update status
        self._is_recording = True
        self.update_available_buttons()
        self.update_status_frame()

        self.driver.record()


    def _clicked_stop(self):
        # Update status
        self._is_reading = False
        self._is_recording = False
        self.update_available_buttons()
        self.update_status_frame()

        self.driver.stop()

    def _clicked_clear(self):
        """
        Ask user for clear confirmation. When confirmed, run clear_confirmed(). This function only prompt user
        for confirmation. the actual function which handles clearing the cache is clear_confirmed().
        """
        # pops out a window to make sure user want to clear all data: 'this will clear all data... u sure?'
        is_he_sure = askyesno(title='Confirmation',
                              message='All unsaved data will be lost. Do you wish to proceed?')
        if is_he_sure == True:
            self._clear_confirmed()

    def _clear_confirmed(self):
        self.driver.plot.root.destroy()
        del self.driver

        # Update status only after clearing is done without breaking
        self._is_cleared = True
        self.update_available_buttons()
        self.update_status_frame()

    def _clicked_path(self):
        folderPath = filedialog.askdirectory()
        self.filePath = folderPath
        print("File Path Selected:", self.filePath)
        # self._ctrl.setFolderPath(folderPath)

    def _clicked_add_plotter(self):
        """
        Add a plotter frame
        :return: None
        """
        self.plotEmpty = False
        self.update_available_buttons()
        if self.plot_frame_container is None:
            self.plot_frame_container = tk.Frame(self)
            self.plot_frame_container.grid(row=2, column=1, columnspan=7, sticky='nw')

        plot_id = len(self._plot_frame_container)
        plot_name = f'Plot {plot_id}'
        plot_frame = PlotFrame(self.plot_frame_container, plot_name)
        plot_frame.pack(side='left', padx=(10, 0))
        # plot_frame.grid(row=2, column=1 + plot_id, sticky='n')
        self._plot_frame_container.append(plot_frame)
        self.update_available_ai()

    def _clicked_remove_plotter(self):
        """
        Remove the last plotter frame
        :return: None
        """
        if self._plot_frame_container:
            self._plot_frame_container[-1].destroy()
            self._plot_frame_container.pop(-1)
            if not self._plot_frame_container:
                self.plot_frame_container.destroy()
                self.plot_frame_container = None
                self.plotEmpty = True
                self.update_available_buttons()

    def _create_driver(self, samp_freq, ao_frames, available_ai, plot_frames, device_name='Dev1', show_graph=False):
        """
        A driver is created here. Writers, readers, and plot_config are created and passed into driver.
        :type samp_freq: float
        :type ao_frames: dict
        :type available_ai: list
        """
        driver = Channel_Driver(self, num=None, sample_rate=samp_freq, show_graphs=show_graph, device_name=device_name)
        driver.addOverflowCallBack(self.dataOverflowCallback)
        writers = []
        for index in self._ao_frame_container.keys():
            frame = ao_frames[index]
            writer = self._create_writer(samp_freq, ao_index=index, ao_frame=frame)
            writers.append(writer)
        driver.add_writer(writers)

        readers = []
        for index in available_ai:
            reader = self._create_reader(ai_index=index, ai_name=f'AI {index}')
            readers.append(reader)
        driver.add_readers(readers)

        plots_config = {}
        for frame in plot_frames:
            plot_config = frame.get_plot_config()
            plots_config.update(plot_config)
        print(plots_config)
        driver.add_custom(plots_config)

        return driver

    @staticmethod
    def _create_writer(samp_freq, ao_index, ao_frame):
        """
        Extracts info from ao_frame, and create a writer object.
        :param samp_freq: here it is used as waveform resolution (points per second)
        :param ao_index: index of AO on the device to send waveform
        :param ao_frame: frame containing info about Waveform
        :return writer: a writer object contains info about one AO.
        :rtype writer: Writer
        """
        # Get writer info
        wave_selection = ao_frame.get_wave_selection()
        wave_params = ao_frame.get_wave_param()
        assert type(wave_selection) is str
        assert type(wave_params) is dict

        # Use WaveFactory to spawn instances of Wave
        wave_factory = WaveFactory()
        wave = wave_factory.create_wave(wave_selection, wave_params, samp_freq)

        # Create Writer instance
        writer = Writer(ao_index, name=f'Writer {ao_index}', waveform=wave)
        return writer

    @staticmethod
    def _create_reader(ai_index, ai_name, time_shown=0.25):
        """
        Create a reader
        :param ai_index: index of AI on the device to be read
        :param ai_name:
        :param time_shown: x-axis domain for Input voltage vs t graph.
        :return:
        """
        reader = Reader(ai_index, ai_name, time_shown)
        return reader

    def _check_input(self):
        if self._ao_frame_container:  # check if ao container is not empty
            self._save.check_empty()  # check if file info is entered
        else:
            messagebox.showerror('Hm', 'Please select some AO to start')
            raise ValueError

    def get_waveforms(self):
        """
        Get waveforms from frames
        :return waveforms: waveforms of each ao
        :rtype waveforms: dict of index:waveform
        """
        waveforms = {}
        for index in self._ao_frame_container.keys():
            waveform = self._ao_frame_container[index].get_wave_selection()
            waveforms.update({index: waveform})
        return waveforms

    @staticmethod
    def get_waveforms_in_str(waveforms):
        """
        Get waveform selection in the style of: 'WF-AO1Tr_AO2Ns_AO3Tr'
        :param waveforms:
        :return: wave_selection_str
        """
        # Get wave and append to name string
        wave_selection_str = 'WF-'
        for index in waveforms.keys():
            wave = waveforms[index][0:1]
            wave_selection_str += f'AO{str(index)}{wave}_'

        # Leave out the last _
        wave_selection_str = wave_selection_str[0:-2]

        return wave_selection_str

    def dataOverflowCallback(self, data):
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print(self.filePath)
        # writeThread = threading.Thread(target=self.writeData, args = (data, None, None, FILEPATH + time + ".tdms"))
        self.writeData(data, None, None, self.filePath + "/" + self.folderName + "/" + self.fileName + time + ".tdms")
        # writeThread.start()

    def writeData(self,dataDict, root, group, filePath):
        print("writeData")
        time1 = tm.time()
        directory = os.path.dirname(filePath)

        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        keys = list(dataDict.keys())
        data = list(dataDict.values())

        with nptdms.TdmsWriter(filePath) as writer:
            # Create channels for each column
            gpName = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            for key, values in zip(keys, data):
                channel = ChannelObject(group=gpName, channel=key, data=values)
                if root and group is not None:
                    writer.write_segment([root, group, channel])
                else:
                    writer.write_segment([channel])

        time2 = tm.time()
        print("Time to write data", time2-time1)
        print("Data has been successfully written to", filePath)
        self.driver.writeThreadRunning = False

    def getSectionTime(self):
        return  self._gen_config.getSectionTime()

    def getSamplesPerChannel(self):
        return  self._gen_config.getSamplesPerChannel()

    # Check the working of this function.
    def is_nidaq_connected(self, device_name):
        try:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan(device_name)
                return True
        except nidaqmx.DaqError:
            return False
