import os
import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self, prefix, trt, rep_num, target):
        self.name = prefix + '-' + trt +'-' +rep_num
        self.dir = 'figures/' + prefix + '/'
        self.target = target
    def find_ylim(self, vec1, vec2):
        min1 = np.amin(vec1)
        max1 = np.amax(vec1)

        min2 = np.amin(vec2)
        max2 = np.amax(vec2)

        return (min1 if min1<min2 else min2,
                max1 if max1>max2 else max2) 
        

    def visualize(self, rep):
        pass

    def save_plot(self, rep, isOne=False):
        if isOne:
            fig = self.plot_one(rep, self.name)
        else:
            fig = self.plot_two(rep, self.name)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        fig.savefig(self.dir + self.name + '.png')

    def plot_two(self, inputdata, name):
        fig, ax = plt.subplots(1,1)
        fig.set_size_inches(15, 5)
        fig.suptitle(name, fontsize=16)

        t = inputdata[:, 0]
        thrust = inputdata[:, 1]
        pressure = inputdata[:, 2]

        ylim = self.find_ylim(thrust, pressure)
        ax.set_ylim(ylim)
        # ax.set_ylim(-1, ylim[1])

        ax.plot(t, thrust, t, pressure)
        ax.grid(True)
        ax.legend(['thrust[N]', 'pressure[bar]'])
        return fig

    def plot_one(self, inputdata, name):
        fig, ax = plt.subplots(1,1)
        fig.set_size_inches(15, 5)
        fig.suptitle(name, fontsize=16)
        t = inputdata[:, 0].tolist()
        y1 = inputdata[:, 1].tolist()
        ax.plot(t, y1, label='mdot[kg/s]')
        ax.grid(True)
        ax.legend()
        return fig

