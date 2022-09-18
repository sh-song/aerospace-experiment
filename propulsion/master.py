#!/usr/bin/python3
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from filters import LowPassFilter as LPF
from preprocessor import Preprocessor
from calculator import Calculator
from plotter import Plotter
def load_data(rawdata_dir, filename):
        trt = filename.split('_')[1]
        file_dir = rawdata_dir + filename
        raw = pd.read_csv(file_dir, sep='\t')
        raw = raw.to_numpy()
        return trt, raw

def generate_data_dict():
    return {'2bar':[], '6bar':[], \
                    '10bar':[], '14bar':[]}

if __name__ == "__main__":
    prefix = 'ttttest'

    #Load raw data
    rawdata = generate_data_dict()    
    rawdata_dir = 'rawdata/'
    filenames = os.listdir(rawdata_dir)
    for filename in filenames:
        trt, raw = load_data(rawdata_dir, filename)
        rawdata[trt].append(raw)


    #Preprocessing
    preprocessed_data = generate_data_dict()
    for trt, replicates in rawdata.items():
        for i, rep in enumerate(replicates):
            pp = Preprocessor(prefix, trt, str(i), rep)
            preprocessed = pp.run()
            preprocessed_data[trt].append(preprocessed)

    # mdot_data = generate_data_dict()
    # for trt, replicates in rawdata.items():
    #     for i, rep in enumerate(replicates):
    #         cc = Calculator(prefix, trt, str(i), rep, 'mdot')
    #         mdot = cc.run()
    #         mdot_data[trt].append(mdot)
    #Plot
    for trt, replicates in rawdata.items():

        for i, rep in enumerate(replicates):
 
            plotter = Plotter(prefix, trt, str(i))
            plotter.save_plot(rep)
    

    print(preprocessed_data)