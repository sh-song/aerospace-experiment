import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from filters import LowPassFilter

class Preprocessor:
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
        
    def filtering(self, data, cutoff):
        lpf = LowPassFilter(cutoff, 0.01)
        filtered = np.zeros(data.shape)
        for i, val in enumerate(data):
            filtered[i] = lpf.filter(val)
        return filtered
    
    def zeroing(self, data):
        target_range = len(data) // 5
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
        # ax.set_ylim(ylim)
        ax.set_ylim(-1, ylim[1])

        ax.plot(t, thrust, t, pressure)
        ax.grid(True)
        ax.legend(['thrust[N]', 'pressure[bar]'])
        #ax.set_aspect('equal', 'box')
        #ax.set_title(name)
        return fig

    def run(self):
        #Low pass filtering
        preprocessed = np.zeros(self.raw.shape)
        preprocessed[:, 0] = self.raw[:, 0]
        preprocessed[:, 1] = self.filtering(self.raw[:, 1], 0.2)
        preprocessed[:, 2] = self.filtering(self.raw[:, 2], 2)

        #Zeroing for thrust
        preprocessed[:, 1] = self.zeroing(preprocessed[:, 1])

        #Scaling
        V_TO_BAR = 10.0512
        V_TO_N = 109.7
        preprocessed[:, 1] = self.convert_scale(preprocessed[:, 1], V_TO_N)
        preprocessed[:, 2] = self.convert_scale(preprocessed[:, 2], V_TO_BAR)
  
        #Plot and Save
        # fig = self.plot(preprocessed, self.name)
        # self.save_plot(fig, self.name)
        return preprocessed