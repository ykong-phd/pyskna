# pyskna/_vfcdm.py (internal binding)

"""
See LICENSE.md for details.
"""


from pathlib import Path
from scipy import signal
import numpy as np
import ctypes
import platform
import struct
from pathlib import Path

_lib = None
_vfcdm1 = None


def load_vfcdmC():
    global _lib, _vfcdm1
    if _lib is not None:
        return  # Already loaded
    # Load the shared library once
    lib_path = get_library_path()
    lib = ctypes.CDLL(str(lib_path.resolve()))

    # Define the C function signature once
    lib.vfcdm1.argtypes = [
        ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), 
        ctypes.POINTER(ctypes.POINTER(ctypes.c_float)), 
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_float),
        ctypes.c_int,
        ctypes.c_float,
        ctypes.POINTER(ctypes.c_float),
        ctypes.POINTER(ctypes.c_float),
        ctypes.c_int,
        ctypes.c_int
    ]
    lib.vfcdm1.restype = ctypes.c_int

    # Export the function
    _vfcdm1 = lib.vfcdm1



def get_library_path():
    """Detect platform and architecture, return path to correct shared library."""
    base = Path(__file__).parent / ".vfcdm"
    system = platform.system()
    bits = struct.calcsize("P") * 8  # 32 or 64

    if system == "Windows":
        fname = f"libvfcdm5_win{bits}.dll"
    elif system == "Linux":
        fname = f"libvfcdm5_linux{bits}.so"
    elif system == "Darwin":
        fname = f"libvfcdm5_mac{bits}.dylib"
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    path = base / fname
    if not path.exists():
        raise FileNotFoundError(f"Shared library not found: {path} / Possibly Unsupported Operating systems or architectures")
    return path


def run_vfcdmC(
        input_ary: np.ndarray, # ECG, 1D array of float32
        filter_len : int, # filter_len for VFCDM
        thread_n: int = 12 # number of thread (1-12)
    ):

    if input_ary.ndim != 1:
        raise ValueError("The input_ary must be a 1D array")
    if thread_n > 12 or thread_n < 1:
        raise ValueError("Thread number should be 1-12")
    
    if _vfcdm1 is None:
        load_vfcdmC()

    data = input_ary.astype(np.float32)
    N = len(data)

    num_channels = 12
    comp1 = (ctypes.POINTER(ctypes.c_float) * num_channels)()
    comp2 = (ctypes.POINTER(ctypes.c_float) * num_channels)()

    for i in range(num_channels):
        comp1[i] = (ctypes.c_float * (N))()
        comp2[i] = (ctypes.c_float * (N))()

    channels = ctypes.c_int()
    # param x
    x = data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    # param for filters
    fw = 0.02
    B = signal.firwin(filter_len, fw*2).astype(np.float32)
    B1 = signal.firwin(filter_len, fw).astype(np.float32)
    B_size = B.size

    
    B = B.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    B1 = B1.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

    _lib.vfcdm1(comp1, comp2, ctypes.byref(channels), x, ctypes.c_int(data.size), ctypes.c_float(fw), B, B1, ctypes.c_int(B_size), ctypes.c_int(thread_n)) 
    
    return_data = np.zeros([num_channels,N])
    
    for i in range(num_channels):
        comp1_data = np.ctypeslib.as_array(comp1[i], shape=(N,))
        
        return_data[i,:] = comp1_data
    
    return return_data
