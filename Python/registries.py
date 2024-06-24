from triangle_wave import TriangleWave
from n_wave import NWave
from user_wave import UserWave


wave_registry = {'Triangular Wave': {'class': TriangleWave,
                              'params': ['Max', 'Min', 'Ramp_Rate', 'Freq'],
                              'default': [1.3, -0.4, 400, 60],
                              'unit': ['Volt', 'Volt', 'Volt/s', 'Hz']},
            'N Wave': {'class': NWave,
                       'params': ['Max', 'Min', 'Hold', 'Ramp_Rate', 'Freq'],
                       'default': [0.6, -0.2, -0.02, 200, 10],
                       'unit': ['Volt', 'Volt', 'Volt', 'Volt/s', 'Hz']},
            'User wave': {'class': UserWave,
                          'params': ['Path'],
                          'default': [None],
                          'unit': ['']}}

device_registry = {'name': 'Dev1',
                   'ai': {'shape': (4,4), 'indexes': [0,1,2,3,4,5,6,7,16,17,18,19,20,21,22,23]},
                   'ao': {'shape': (4,1), 'indexes': [0,1,2,3]}}

# File save path can be relative of definitive. Needs to be a string. If path is invalid, default path will be
# Documents folder
savepath = '../../../../data/'
