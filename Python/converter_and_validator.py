from tkinter import messagebox
import os

import nidaqmx




def convert_to_float(obj, obj_name='Input'):
    """
    Try to convert an object into float. Except: show a messagebox of the error and raise TypeError
    :rtype: float
    """
    try:
        flt = float(obj)
        return flt
    except:
        messagebox.showerror(message=f'Wrong Type: {obj_name} must be a number.')
        raise ValueError


def convert_to_int(obj, obj_name='Input'):
    """
    Try to convert an object into int. Except: show a messagebox of the error and raise TypeError
    :rtype: int
    """
    try:
        flt = float(obj)
        rounded = round(flt)
        return rounded
    except:
        messagebox.showerror(message=f'Wrong Type: {obj_name} must be a integer.')
        raise ValueError


def check_valid_path(param_dict):
    path = param_dict['path']
    is_exist = os.path.exists(path)
    if not is_exist:
        messagebox.showerror(message='Please enter valid path')
        raise ValueError


def check_shape(shape, indexes, obj_name='Input'):
    if not len(indexes) == shape[0] * shape[1]:
        messagebox.showerror(message=f"Shape and number of indexes of {obj_name} doesn't match! Please check device registry.")
        raise ValueError
