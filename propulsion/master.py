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
from csv_saver import CSVSaver
import matplotlib.image
import cv2
from anova import ANOVA
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

    trt_names = ['2bar', '6bar', '10bar', '14bar']
    #Load raw data
    rawdata = generate_data_dict()    
    rawdata_dir = 'rawdata/'
    filenames = os.listdir(rawdata_dir)
    data_shapes = generate_data_dict()
    for filename in filenames:
        trt, raw = load_data(rawdata_dir, filename)
        rawdata[trt].append(raw)
        data_shapes[trt].append(raw.shape)

    #1-1 Preprocessing

    prefix = 'preprosecessed'
    preprocessed_data = generate_data_dict()
    for trt, replicates in rawdata.items():
        for i, rep in enumerate(replicates):
            pp = Preprocessor(prefix, trt, str(i), rep)
            preprocessed = pp.run()
            preprocessed_data[trt].append(preprocessed)

    #1-2 mdot

    prefix = 'mdot'
    mdot_data = generate_data_dict()
    for trt, replicates in preprocessed_data.items():
        for i, rep in enumerate(replicates):
            cc = Calculator(prefix, trt, str(i), rep)
            output = cc.run('mdot')
            mdot_data[trt].append(output)

    #1-3 P_e
    prefix = 'P_e'
    P_e_data = generate_data_dict()
    for trt, replicates in preprocessed_data.items():
        for i, rep in enumerate(replicates):
            cc = Calculator(prefix, trt, str(i), rep)
            output = cc.run('exit_pressure')
            P_e_data[trt].append(output)

    #2-1 
    prefix = 'thrust'
    mdot_and_P_e_data = generate_data_dict()
    for trt in trt_names:
        for i in range(3):
            new_data = np.zeros(data_shapes[trt][i])
            new_data[:, 0] = mdot_data[trt][i][:, 0].copy()
            new_data[:, 1] = mdot_data[trt][i][:, 1].copy()
            new_data[:, 2] = P_e_data[trt][i][:, 1].copy()
            mdot_and_P_e_data[trt].append(new_data)

    thrust_data = generate_data_dict()
    for trt, replicates in mdot_and_P_e_data.items():
        for i, rep in enumerate(replicates):
            cc = Calculator(prefix, trt, str(i), rep)
            output = cc.run('thrust')
            thrust_data[trt].append(output)

    #2-2
    prefix = 'thrust_compare'
    thrust_compare_data = generate_data_dict()
    for trt in trt_names:
        for i in range(3):
            new_data = np.zeros(data_shapes[trt][i])
            new_data[:, 0] = mdot_data[trt][i][:, 0].copy()
            new_data[:, 1] = preprocessed_data[trt][i][:, 1].copy()
            new_data[:, 2] = thrust_data[trt][i][:, 1].copy()
            thrust_compare_data[trt].append(new_data)


    # #Additional experiment
    # prefix = 'additional_exp_1'
    # anova_table_data = generate_data_dict()
    # for trt in trt_names:
    #     for i in range(3):
    #         new_data = np.zeros(data_shapes[trt][i])
    #         input = thrust_data[trt][i][:, 1].copy()
    #         anova = ANOVA(input)
    #         result = anova.run()
    #         new_data[:, 0] = mdot_data[trt][i][:, 0].copy()
    #         new_data[:, 1] = preprocessed_data[trt][i][:, 1].copy()
    #         new_data[:, 2] = thrust_data[trt][i][:, 1].copy()
    #         anova_table_data[trt].append(new_data)


    #save result
    prefix = 'preprocessed'
    total_fig = np.zeros([500*4, 1500*3, 4])
    i = 0
    for trt, replicates in preprocessed_data.items():########
        for j, rep in enumerate(replicates):
            plotter = Plotter(prefix, trt, j)
            fig = plotter.make_plot(rep, False)
            fig.canvas.draw()
            X = np.array(fig.canvas.renderer.buffer_rgba())
            total_fig[500*i:500*(i+1), 1500*j:1500*(j+1), :] = X
            plt.close(fig)
        i +=1
           
    cv2.imwrite('figures/' + prefix+ '.png', total_fig)

    #save csv
    for trt, replicates in preprocessed_data.items():#########
        for i, rep in enumerate(replicates):
            saver = CSVSaver(prefix, trt, str(i))
            saver.save_csv(rep)
    #i