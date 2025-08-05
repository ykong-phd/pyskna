# pyskna
This toolbox provides computation methods for skin nerve activity (SKNA), which can be derived from electrocardiogram (ECG) signals collected under specific recording conditions.

## Installation

```bash
pip install pyskna
```

## Example



```python
import pandas as pd
from pyskna import extract_iSKNA, extract_TVSKNA

# Load EKG file
EKG = pd.read_csv("example_ekg.csv", header=None).to_numpy().reshape(-1)

# iSKNA computation
SKNA_dict = extract_iSKNA(input_ary=EKG, fs=4000, f_l=500, f_h=1000, smoothing_win_len=0.1)

# TVSKNA computation
TVSKNA_dict = extract_TVSKNA(input_ary=EKG, fs=4000, smoothing_win_len=0.1, thread_n=12)

```
See [`test.py`](./tests/test.py)

## Compatibility for extract_TVSKNA
The extract_TVSKNA function uses VFCDM binaries, which has been tested with **Python 3.11** on the following platforms:
- macOS (Apple Silicon / ARM64) 
- Linux (x86_64)
- Windows (x86_64)

### Notes
- macOS x86_64 (Intel) **is expected to work**, but has not been formally tested.
- 32-bit systems are **not supported**; the VFCDM library has only been compiled for 64-bit architectures.

## Citation
The neuECG technique for computing iSKNA has been implemented based on the following paper:
### iSKNA:
Kusayama, T., Wong, J., Liu, X., He, W., Doytchinova, A., Robinson, E. A., ... & Chen, P. S. (2020).  
*Simultaneous noninvasive recording of electrocardiogram and skin sympathetic nerve activity (neuECG).*  
**Nature Protocols**, 15(5), 1853–1877.

### TVSKNA:
If you use TVSKNA for 4kHz sampling frequency. Please cite the following paper:

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




### ⚠️ Patent Notice

Some functions (e.g., **`process_tvskna`**) in this library interface with the **VFCDM** algorithm covered by  
U.S. Patent No. **US8858450B2**, owned by Ki Chon, Ph.D. and Kihwan Ju, Ph.D.  
(Assignee: Research Foundation of the State University of New York).

By using VFCDM‑related functions (e.g., **`process_tvskna`**) in PySKNA, you agree to the  
[LICENSE.md](https://github.com/ykong-phd/vfcdm-binaries/blob/main/LICENSE.md) and [PATENT_NOTICE.md](https://github.com/ykong-phd/vfcdm-binaries/blob/main/PATENT_NOTICE.md) provided in the VFCDM Binaries repository, **solely for non-commercial, academic, and research use**.

 

Please see the PySKNA `LICENSE.md` for more details.

Commercial use of the patented components requires a separate license.  

For patent‑related inquiries, contact **ki.chon@uconn.edu**.  

For all other matters, contact **youngsun.kong.phd@gmail.com**.
