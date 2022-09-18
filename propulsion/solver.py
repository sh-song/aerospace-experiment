import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from filters import LowPassFilter

class Solver:
    def __init__(self, prefix, trt, rep_num, data):
        self.name = prefix + '-' + trt +'-' +rep_num
        self.dir = 'figures/' + prefix + '/'
        self.raw = data
        self.filtered_data = None


    def convert_scale(self, vector, scalefactor):
        return vector * scalefactor

    def save_plot(self, fig, name):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        fig.savefig(self.dir+name+'.png')

    def find_ylim(self, vec1, vec2):
        min1 = np.amin(vec1)
        max1 = np.amax(vec1)

        min2 = np.amin(vec2)
        max2 = np.amax(vec2)

        return (min1 if min1<min2 else min2,
                max1 if max1>max2 else max2) 
        
    def filtering(self, data):
        lpf = LowPassFilter(2, 0.01)
        filtered = np.zeros(data.shape)
        for i, val in enumerate(data):
            print(i, val)
            filtered[i] = lpf.filter(val)
        return filtered
    
    def zeroing(self, data):
        target_range = len(data) // 10
        front_mean = np.mean(data[:target_range])
        back_mean = np.mean(data[target_range:])
        offset = (front_mean + back_mean) / 2
        return data - offset

    def plot(self, inputdata, name):
        fig, ax = plt.subplots(1,1)
        fig.set_size_inches(15, 5)
        fig.suptitle(name, fontsize=16)

        t = inputdata[:, 0]
        thrust = inputdata[:, 1]
        pressure = inputdata[:, 2]

        ylim = self.find_ylim(thrust, pressure)
        ax.set_ylim(ylim)
        ax.set_ylim(-0.02, ylim[1])

        ax.plot(t, thrust, t, pressure)
        ax.grid(True)
        ax.legend(['thrust[V]', 'pressure[V]'])
        #ax.set_aspect('equal', 'box')
        #ax.set_title(name)
        return fig

    def run(self):
        #Low pass filtering
        filtered = np.zeros(self.raw.shape)
        filtered[:, 0] = self.raw[:, 0]
        filtered[:, 1] = self.filtering(self.raw[:, 1])
        filtered[:, 2] = self.filtering(self.raw[:, 2])

        #Zeroing for thrust
        filtered[:, 1] = self.zeroing(filtered[:, 1])
        fig = self.plot(filtered, self.name)
        self.save_plot(fig, self.name)