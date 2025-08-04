# API Reference

This document describes the main functions available in the `pySKNA` library.

---

## `extract_SKNA(...)`

Extracts the **integrated Skin Sympathetic Nerve Activity (iSKNA)** using bandpass filtering and smoothing from a 1D ECG-derived signal.

### Parameters:
- **input_ary** (*np.ndarray*): 1D NumPy array of type `float32`, typically an ECG signal.  
  *Note: Many ECG devices apply built-in filtering, which may attenuate or remove SKNA components.*
- **fs** (*int*): Sampling frequency in Hz.
- **f_l** (*float*, optional): Lower cutoff frequency for bandpass filtering (default: `500` Hz).
- **f_h** (*float*, optional): Upper cutoff frequency for bandpass filtering (default: `1000` Hz), # (None for highpass).
- **smoothing_win_len** (*float*, optional): Length of the moving average smoothing window in seconds (default: `0.1`).

### Returns:
A dictionary containing:
- **FilteredEKG** (*np.ndarray*): The bandpass-filtered ECG signal.
- **iSKNA** (*np.ndarray*): The integrated SKNA signal after rectification and smoothing.

### Reference:
Kusayama, T., Wong, J., Liu, X., He, W., Doytchinova, A., Robinson, E. A., ... & Chen, P. S. (2020).  
*Simultaneous noninvasive recording of electrocardiogram and skin sympathetic nerve activity (neuECG).*  
**Nature Protocols**, 15(5), 1853–1877.

---

## `extract_TVSKNA(...)`

Extracts the **time-varying Skin Sympathetic Nerve Activity (TVSKNA)** using Variable Frequency Complex Demodulation (VFCDM) from a 1D ECG-derived signal.

- **VFCDM reference:**
    
    Wang, H., Siu, K., Ju, K., & Chon, K. H. (2006).
    *A high resolution approach to estimating time-frequency spectra and their amplitudes.*
    **Annals of biomedical engineering, 34(2), 326-338**.

### Parameters:
- **input_ary** (*np.ndarray*): 1D NumPy array of type `float32`, typically an ECG signal.
  *Note: Many ECG devices apply built-in filtering, which may attenuate or remove SKNA components.*
- **fs** (*int*): Sampling frequency in Hz. Must be one of: `500`, `1000`, or `4000`.
- **smoothing_win_len** (*float*, optional): Length of the smoothing window in seconds (default: `0.1`).
- **thread_n** (*int*, optional): Number of parallel threads to use (default: `12`). Acceptable range: 1–12.
- **verbose** (*int*, optional): Verbosity level (default: `1`). Set to `1` to display progress messages; `0` for silent mode.

### Returns:
A dictionary with the following keys, depending on the sampling frequency:

#### For 1000 Hz and 4000 Hz sampling:
Multiple frequency bands are extracted. The dictionary includes:

- **TVSKNA1_signal** (*np.ndarray*): Time-varying SKNA signal for frequency band 1.
- **TVSKNA1_freq** (*str*): Label for frequency band 1 (e.g., `"500–1000 Hz"`).

- **TVSKNA2_signal** (*np.ndarray*): Time-varying SKNA signal for frequency band 2.
- **TVSKNA2_freq** (*str*): Label for frequency band 2.

- **TVSKNA3_signal** (*np.ndarray*): Time-varying SKNA signal for frequency band 3.
- **TVSKNA3_freq** (*str*): Label for frequency band 3.

#### For 500 Hz sampling:
Only a single frequency band is extracted. The dictionary includes:

- **TVSKNA_signal** (*np.ndarray*): Time-varying SKNA signal.
- **TVSKNA_freq** (*str*): Frequency band label (e.g., `"150–250 Hz"`).

### References:
- **For 4 kHz sampling:**

  Kong, Y., Baghestani, F., D'Angelo, W., Chen, I. P., & Chon, K. H. (2025).  
  *A New Approach to Characterize Dynamics of ECG-Derived Skin Nerve Activity via Time-Varying Spectral Analysis.*  
  **IEEE Transactions on Affective Computing**.

- **For 500 and 1000 Hz sampling:**

  Kong, Y., Baghestani, F., D'Angelo, W., Chen, I. P., & Chon, K. H. (2025).  
  *A New Approach to Characterize Dynamics of ECG-Derived Skin Nerve Activity via Time-Varying Spectral Analysis.*  
  **IEEE Transactions on Affective Computing**.

  Kong, Y., Baghestani, F., Chen, I. P., & Chon, K. H. (2025).  
  *Feasibility of Extracting Skin Nerve Activity from Electrocardiogram Recorded at a Low Sampling Frequency.*  
  **arXiv preprint**, arXiv:2508.00494. https://doi.org/10.48550/arXiv.2508.00494

---