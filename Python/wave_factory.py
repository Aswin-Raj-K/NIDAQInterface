from registries import wave_registry


class WaveFactory:
    def __init__(self):
        """
        Implementation of a wave factory.
        Parameters:
        - wave_register: Python dictionary, which keeps track of the currently available wave forms in form of key-value pairs, where the key is the name of the wave form and value is the creator of the wave form
        """
        # initialization of register
        self._wave_register = wave_registry

    def register_wave(self, wave_name, wave_creator):
        """
        Function to update the Python dictionary of available wave forms.
        Input:
        - wave_name: key of the creator of the wave form
        - wave_creater: creator of the wave form
        """
        
        self._wave_register[wave_name] = wave_creator

    def create_wave(self, wave_name, params, samp_freq):
        """
        Creation of voltage wave
        - wave_name: name of the voltage signal used as the key to the wave register
        - params: Python dictionary including all needed parameters to initiate the wave of type wave_name
        """
        return self._wave_register[wave_name]['class'](**params, samp_freq=samp_freq)
