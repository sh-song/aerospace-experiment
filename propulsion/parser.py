#!/usr/bin/python3
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from filters import LowPassFilter as LPF
def load_data(rawdata_dir):
        V_TO_BAR = 10.0512
        V_TO_N = 109.7

        filenames = os.listdir(rawdata_dir)
        data = {'2bar':[], '6bar':[], \
                    '10bar':[], '14bar':[]}

        for filename in filenames:
            treatment = filename.split('_')[1]
            file_dir = rawdata_dir + filename
            raw = pd.read_csv(file_dir, sep='\t')
            raw = raw.to_numpy()
            # Conver scale 
            raw[:, 1] = convert_scale(raw[:, 1], V_TO_N)
            raw[:, 2] = convert_scale(raw[:, 2], V_TO_BAR)
            data[treatment].append(raw)

        return data
def save_plot(fig, prefix, name):
    fig.savefig('figures/'+prefix+'_'+name+'.png')

def convert_scale(vector, scalefactor):
    return vector * scalefactor

def visualize(replicates, name):
    fig, axs = plt.subplots(1,3)
    fig.set_size_inches(15, 5)
    fig.suptitle(name, fontsize=16)

    for i, rep in enumerate(replicates):
        t = rep[:, 0]
        thrust = rep[:, 1]
        pressure = rep[:, 2]

        axs[i].plot(t, thrust, t, pressure)
        axs[i].grid(True)
        axs[i].set_ylim(-10, 5)
        axs[i].legend(['thrust[N]', 'pressure[bar]'])
        #axs[i].set_aspect('equal', 'box')
        axs[i].set_title(f"rep {i}")
    #fig.tight_layout()
    save_plot(fig, 'filtered', name)
if __name__ == "__main__":
    data = load_data('rawdata/')

    for treatment, replicates in data.items():
        print(treatment)

        visualize(replicates, treatment)
