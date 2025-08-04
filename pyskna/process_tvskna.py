# pyskna/process.py
import numpy as np

import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
from typing import Dict
from scipy import signal
from typing import Literal
from datetime import datetime
from ._vfcdm import run_vfcdmC




def ECG_filt_HF150(sig,fs):
    cutoff = 150   # Passband frequency
    fstop  = 130   # Stopband frequency
    
    attenuation = 60 # Stopband attenuation (dB) (default: 60)

    # Calculate transition width
    width = cutoff - fstop

    # Estimate filter order using kaiserord
    numtaps, beta = signal.kaiserord(attenuation, width / (0.5 * fs))

    # Ensure numtaps is odd
    if numtaps % 2 == 0:
        numtaps += 1

    b = signal.firwin(numtaps, cutoff = cutoff / (fs/2), window=('kaiser', beta), pass_zero=False); a = 1

    filtered_sig = signal.filtfilt(b,a,sig)
    return filtered_sig


def filt_hilbert_reconst(x,smoothing_win_len, verbose) :
    if verbose > 0:
        print('running Hilbert transform')
        start=datetime.now()
    hilbert_x = signal.hilbert(x/np.std(x))
    if verbose > 0:
        print('Hilbert transform runtime: ', datetime.now()-start)
    return uniform_filter1d(np.abs(hilbert_x),size=smoothing_win_len)


def extract_TVSKNA(
        input_ary: np.ndarray, # ECG, 1D array of float32
        fs: int = Literal[500, 1000, 4000], # sampling frequency
        smoothing_win_len : float = 0.1, # window second (second)
        thread_n : int = 12, # number of thread (1-12)
        verbose : int = 1 # verbose = 0 or 1
        ) -> Dict[str, float]:
    
    if input_ary.ndim != 1:
        raise ValueError("The input_ary must be a 1D array")
    if thread_n > 12 or thread_n < 1:
        raise ValueError("Thread number should be 1-12")
    

    input_ary1 = input_ary.copy()

    #### VFCDM features
    filtered_ekg = ECG_filt_HF150(input_ary1,fs)


    comp1 = np.zeros([12,len(filtered_ekg)])

    if fs == 500:
        filter_len = 32
    else:
        filter_len = 4000

    if verbose > 0:
        print('running VFCDM')
        start=datetime.now()

    comp1[:, :] = run_vfcdmC(filtered_ekg, filter_len, thread_n)

    if verbose > 0:
        print('VFCDM runtime: ', datetime.now()-start)
        
    return_dict = {}
    if fs == 4000:
        return_dict['TVSKNA1_signal'] = filt_hilbert_reconst(np.sum(comp1[1:7,:],axis=0), int(smoothing_win_len * fs), verbose = verbose)
        return_dict['TVSKNA2_signal'] = filt_hilbert_reconst(np.sum(comp1[2:7,:],axis=0), int(smoothing_win_len * fs), verbose = verbose)
        return_dict['TVSKNA3_signal'] = filt_hilbert_reconst(np.sum(comp1[3:7,:],axis=0), int(smoothing_win_len * fs), verbose = verbose)

        return_dict['TVSKNA1_freq'] = "160 - 1120 Hz"
        return_dict['TVSKNA2_freq'] = "320 - 1120 Hz"
        return_dict['TVSKNA3_freq'] = "480 - 1120 Hz"
    elif fs == 1000:
        return_dict['TVSKNA1_signal'] = filt_hilbert_reconst(np.sum(comp1[4:12,:],axis=0), int(smoothing_win_len * fs), verbose = verbose)
        return_dict['TVSKNA2_signal'] = filt_hilbert_reconst(np.sum(comp1[6:12,:],axis=0), int(smoothing_win_len * fs), verbose = verbose)
        return_dict['TVSKNA3_signal'] = filt_hilbert_reconst(np.sum(comp1[9:12,:],axis=0), int(smoothing_win_len * fs), verbose = verbose)

        return_dict['TVSKNA1_freq'] = "160 - 480 Hz"
        return_dict['TVSKNA2_freq'] = "240 - 480 Hz"
        return_dict['TVSKNA3_freq'] = "360 - 480 Hz"
    elif fs == 500:
        return_dict['TVSKNA_signal'] = filt_hilbert_reconst(np.sum(comp1[8:12,:],axis=0), int(smoothing_win_len * fs), verbose = verbose)
        return_dict['TVSKNA_freq'] = "160 - 240 Hz"
    else:
        raise ValueError("FS should be 500, 1000, or 4000 Hz")


    return return_dict