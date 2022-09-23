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

def get_sample_range():
    sr= generate_data_dict()
    sr['2bar'] = [[3.2, 4.1], [4.1, 5.6], [3.9, 5.2]]
    sr['6bar'] = [[2.8, 3.4], [2.0, 2.7], [1.0, 1.7]]
    sr['10bar'] = [[2.2, 2.8], [1.9, 2.6], [2.0, 2.7]]
    sr['14bar'] = [[1.5, 2.5], [2.2, 3.0], [1.5, 2.3]]
    return sr


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

    prefix = 'thrust_residual_plot'
    thrust_sample_compare_data = generate_data_dict()
    sample_range = get_sample_range()
    for trt in trt_names:
        for i in range(3):
 
            start = int(sample_range[trt][i][0]*10000)
            end = int(sample_range[trt][i][1]*10000)

            length = end - start
            new_data = np.zeros([length, 2])
            # new_data[:, 0] = mdot_data[trt][i][:, 0].copy()
            new_data[:, 0] = np.array(range(length))
            new_data[:, 1] = thrust_data[trt][i][start:end, 1].copy() - preprocessed_data[trt][i][start:end, 1].copy() 
            # new_data[:, 2] = thrust_data[trt][i][start:end, 1].copy()
            thrust_sample_compare_data[trt].append(new_data)

    #SST, SSR, SSE
    anova = generate_data_dict()
        
    def get_ANOVA(y_hat, y):

        n = y.shape[0]
        y_bar = np.ones(n, dtype=np.float64) * np.mean(y)

        SSE = np.sum((y_hat - y_bar)**2)
        SSR = np.sum((y - y_hat)**2)
        SST = SSE + SSR
        R_squared = SSE / SST
        R_squared = 1 - (SSR / (n - 2) )/ (SST / (n - 1))
        return SST, SSE, SSR, R_squared
    #ANOVA for 2-2     
    for trt in trt_names:
        for i in range(3):
            start = int(sample_range[trt][i][0]*10000)
            end = int(sample_range[trt][i][1]*10000)
            y_hat =  thrust_data[trt][i][start:end, 1].copy() #estimated
            y = preprocessed_data[trt][i][start:end, 1].copy() #measured

            # anova[trt] = get_ANOVA(y_hat, y)
            SST, SSE, SSR, R_squared = get_ANOVA(y_hat, y)

            
            print(f"{trt}-{i+1}---SST: {SST}, SSE: {SSE}, SSR: {SSR}, R_squared: {R_squared}")



            
 


    #Additional experiment
    prefix = 'additional_exp_1'
    anova_table_data = generate_data_dict()
    for trt in trt_names:
        for i in range(3):
            new_data = np.zeros(data_shapes[trt][i])
            start = int(sample_range[trt][i][0]*10000)
            end = int(sample_range[trt][i][1]*10000)
            sample = thrust_data[trt][i][start:end, 1].copy()
            anova_table_data[trt].append(np.mean(sample))
 
    total_mean = 0.0
    for trt in trt_names:
        trt_mean = np.mean(np.array(anova_table_data[trt]))
        anova_table_data[trt].append(trt_mean)
        total_mean += trt_mean / 4

    SS_trt = 0.0
    SS_E = 0.0
    SS_T = 0.0
    for trt in trt_names:
        for i in range(0,3):
            trt_mean = anova_table_data[trt][3]
            SS_T += (anova_table_data[trt][i] - total_mean)**2
            SS_trt += (trt_mean - total_mean)**2
            SS_E += (anova_table_data[trt][i] - trt_mean)**2
    # SS_T = SS_trt + SS_E 

    R = SS_trt / SS_T

    n = 12
    R = 1 - (SS_E / (n - 2) )/ (SS_T / (n - 1))
    print(f"Additional Experiment Result --- SST: {SS_T}, SSE: {SS_E}, SStrt: {SS_trt}, R_squared: {R}")
    
            # print(len(result))



    #save result
    # total_fig = np.zeros([500*4, 1500*3, 4])
    # i = 0
    # for trt, replicates in thrust_sample_compare_data.items():########
    #     for j, rep in enumerate(replicates):
    #         plotter = Plotter(prefix, trt, j)
    #         fig = plotter.make_plot(rep, True)
    #         fig.canvas.draw()
    #         X = np.array(fig.canvas.renderer.buffer_rgba())
    #         total_fig[500*i:500*(i+1), 1500*j:1500*(j+1), :] = X
    #         plt.close(fig)
    #     i +=1
           
    # cv2.imwrite('figures/' + prefix+ '.png', total_fig)

    # #save csv
    # for trt, replicates in preprocessed_data.items():#########
    #     for i, rep in enumerate(replicates):
    #         saver = CSVSaver(prefix, trt, str(i))
    #         saver.save_csv(rep)
    # #i