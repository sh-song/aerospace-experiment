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
import numpy.linalg as npl
def load_data(rawdata_dir, filename):
        trt = filename.split('.')[0]
        file_dir = rawdata_dir + filename
        raw = pd.read_csv(file_dir, sep=' ')
        raw = raw.to_numpy()
        return trt, raw

if __name__ == "__main__":

    rawdata_dir = 'rawdata/'
    filenames = os.listdir(rawdata_dir)
    trt_names = [filename.split('.')[0] for filename in filenames]

    def generate_data_dict():
        global trt_names
        out = {}
        for trt_name in sorted(trt_names):
            out[trt_name] = []
        return out
            
   #Load raw data

    rawdata = generate_data_dict()    
    data_shapes = generate_data_dict()
    for filename in filenames:
        trt, raw = load_data(rawdata_dir, filename)
        rawdata[trt].append(raw)
        data_shapes[trt].append(raw.shape)

    # lift
    target = 'Lift Coefficient'
    lift_coeff_data = generate_data_dict()
    for trt, data in rawdata.items():
        cc = Calculator(target, trt, data[0])
        output = cc.run(target)
        lift_coeff_data[trt].append(output)


    #drag
    target = 'Drag Coefficient'
    drag_coeff_data = generate_data_dict()
    for trt, data in rawdata.items():
        cc = Calculator(target, trt, data[0])
        output = cc.run(target)
        drag_coeff_data[trt].append(output)

    # mmnt
    target = 'Pitching Moment Coefficient'
    pitching_mmnt_data = generate_data_dict()

    for trt, data in rawdata.items():
        cc = Calculator(target, trt, data[0])
        output = cc.run(target)
        pitching_mmnt_data[trt].append(output)

    for trt, output in pitching_mmnt_data.items():
        title = f"Pitching Moment for {trt} degrees"
        ys = output

        fig, ax = plt.subplots(1,1)
        fig.set_size_inches(15, 5)
        fig.suptitle(title, fontsize=16)

        xs = [i for i in range(len(ys[0]))]
        print(len(ys), len(xs))
        ax.scatter(xs,ys, label="")
        ax.grid(True)
        ax.legend()

        ax.set_xlabel('Time')
        ax.set_ylabel('Pitching Moment')

        fig.canvas.draw()
        plt.show()

    # title = "Linear Fitting for Lift Coefficient"
    # fig, ax = plt.subplots(1,1)
    # fig.set_size_inches(15, 5)
    # fig.suptitle(title, fontsize=16)

    # b = []

    # aoa = [-4, -2, 0, 2, 4, 6, 8]
    # A = np.array([aoa, 
    #             [1, 1, 1, 1, 1, 1, 1]]).T

    # for trt, mean in lift_coeff_data.items():
    #     b.append(mean[0])
    # b = np.array(b)
    # m, n = npl.lstsq(A, b, rcond=None)[0]

    

    # func = lambda x : m*x + n
    # line_x = np.arange(-4, 8, 0.05)
    # line_y = [0.0] * len(line_x)
    # for i, x in enumerate(line_x):
    #     line_y[i] = func(x)
    
    # print(aoa)
    # print(b)
    # print(f"m,n:{m} {n}")
    # ax.scatter(line_x, line_y, label="Fitted line using least squares method")
    # ax.scatter(np.array(aoa), b, label="Estimate from measured data")
    # for i, trt in enumerate(sorted(trt_names)):
    #     ax.annotate(f"   AoA: {trt}°", (aoa[i], b[i]))
    # ax.grid(True)
    # ax.legend()

    # ax.set_xlabel('Angle of Attack')
    # ax.set_ylabel('Lift Coefficient')

    # fig.canvas.draw()
    # plt.show()
