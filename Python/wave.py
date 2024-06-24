import abc


class Wave(abc.ABC):
    """
    Abstract base class describing Wave interface.
    Wave should be:
    + initialized with and store any necessary parameters;
    + have a get_wave() method with signature get_wave(freq)
    """
    @abc.abstractmethod
    def __init__(self, repetition_freq):
        pass

    @abc.abstractmethod
    def get_array(self):
        '''
        Function that creates the voltage signal.

        Returns:

        wave: time-voltage signal (numpy array) DO WE NEED TO RETURN THE TIME AT ALL?

        '''
        pass
