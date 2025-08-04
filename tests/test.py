# test.py
# %%

import pandas as pd
from pyskna import extract_iSKNA, extract_TVSKNA
import matplotlib.pyplot as plt


def test_iSKNA(EKG):
    
    SKNA_dict = extract_iSKNA(input_ary=EKG, fs=4000, f_l=500, f_h=1000, smoothing_win_len=0.1)

    fig,ax = plt.subplots(2,1)
    ax[0].plot(EKG)
    ax[0].set_ylabel("EKG")

    ax[1].plot(SKNA_dict['iSKNA'])
    ax[1].set_ylabel("iSKNA")

    ax[1].set_xlabel('Samples')
    plt.show()

def test_TVSKNA(EKG):
    
    SKNA_dict = extract_TVSKNA(input_ary=EKG, fs=4000, smoothing_win_len=0.1,thread_n = 12)

    fig,ax = plt.subplots(2,1)
    ax[0].plot(EKG)
    ax[0].set_ylabel("EKG")

    ax[1].plot(SKNA_dict['TVSKNA1_signal'])
    ax[1].set_ylabel("TVSKNA")

    ax[1].set_xlabel('Samples')
    plt.show()


if __name__ == "__main__":
    EKG = pd.read_csv("example_ekg.csv",header=None).to_numpy().reshape(-1)
    test_iSKNA(EKG)
    test_TVSKNA(EKG)
# %%
