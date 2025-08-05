# pyskna/process.py
import numpy as np
from scipy import signal
from os.path import join
from scipy.ndimage import uniform_filter1d
from typing import Dict

def extract_iSKNA(
        input_ary: np.ndarray, # ECG, 1D array of float32
        fs: int, # sampling frequency
        f_l: float = 500, # Bandpass (lower cutoff)
        f_h: float = 1000, # Bandpass (higher cutoff, or None for highpass)
        smoothing_win_len : float = 0.1 # window second (second)
        ) -> Dict[str, float]:
    
    if input_ary.ndim != 1:
        raise ValueError("The input_ary must be a 1D array")
    
    if f_h >= fs / 2 or f_l >= fs / 2:
        raise ValueError("The cutoff frequencies should be below fs/2, according to the Nyquist theorem.")
    
    if f_h is None:
        pass
    elif not f_l < f_h:
        raise ValueError("The bandpass low cutoff should be below high cutoff")
    
    if f_h < fs / 2:
        # Define parameters
        fpass = [f_l, f_h] # Passband frequency

        fstop_a = (f_h - f_l) * 0.05
        fstop = [f_l - fstop_a, f_h + fstop_a ] # Stopband frequency
        
        attenuation = 60 # Stopband attenuation (dB) (default: 60)

        # Calculate transition width
        width = min(fpass[0] - fstop[0], fstop[1] - fpass[1])

        # Estimate filter order using kaiserord
        numtaps, beta = signal.kaiserord(attenuation, width / (0.5 * fs))

        
        b = signal.firwin(numtaps, cutoff=fpass, window=('kaiser', beta), pass_zero='bandpass', fs=fs); a = 1

        SKNA = 1e6 * signal.filtfilt(b,a,input_ary)

    else: # Highpass filter
        # Define parameters
        cutoff = f_l # Passband frequency

        fstop_a = (fs/2 - f_l) * 0.05
        fstop = f_l - fstop_a # Stopband frequency
        
        attenuation = 60 # Stopband attenuation (dB) (default: 60)

        # Calculate transition width
        width = cutoff - fstop

        # Estimate filter order using kaiserord
        numtaps, beta = signal.kaiserord(attenuation, width / (0.5 * fs))
        if numtaps % 2 == 0:
            numtaps += 1

        b = signal.firwin(numtaps, cutoff = cutoff / (fs/2), window=('kaiser', beta), pass_zero=False); a = 1

        SKNA = 1e6 * signal.filtfilt(b,a,input_ary)


    SKNArec = abs(SKNA); # rectifier
    iSKNA = uniform_filter1d(SKNArec,int(smoothing_win_len*fs))

    return_dict = {}
    return_dict['FilteredEKG'] = SKNA
    return_dict['iSKNA'] = iSKNA

    return return_dict