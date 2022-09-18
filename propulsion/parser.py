#!/usr/bin/python3
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from filters import LowPassFilter as LPF
from solver import Solver
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
            # Convert scale 
            #raw[:, 1] = convert_scale(raw[:, 1], V_TO_N)
            #raw[:, 2] = convert_scale(raw[:, 2], V_TO_BAR)
            data[treatment].append(raw)

        return data

if __name__ == "__main__":
    data = load_data('rawdata/')
    prefix = 'raw-ylim_fixed'
    for treatment, replicates in data.items():
        for i, rep in enumerate(replicates):
            ss = Solver(prefix, treatment, str(i), rep)
            ss.run()
