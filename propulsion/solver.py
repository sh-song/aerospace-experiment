import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from filters import LowPassFilter as LPF

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
        
    def plot(self, inputdata, name):
        fig, ax = plt.subplots(1,1)
        fig.set_size_inches(15, 5)
        fig.suptitle(name, fontsize=16)

        t = inputdata[:, 0]
        thrust = inputdata[:, 1]
        pressure = inputdata[:, 2]

        ylim = self.find_ylim(thrust, pressure)
        ax.set_ylim(-0.05, ylim[1])

        ax.plot(t, thrust, t, pressure)
        ax.grid(True)
        ax.legend(['thrust[V]', 'pressure[V]'])
        #ax.set_aspect('equal', 'box')
        #ax.set_title(name)
        return fig

    def run(self):
        fig = self.plot(self.raw, self.name)
        self.save_plot(fig, self.name)