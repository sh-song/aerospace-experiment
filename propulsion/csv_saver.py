import numpy as np
import os

class CSVSaver:
    def __init__(self, prefix, trt, rep_num):
        self.name = prefix + '-' + trt +'-' +rep_num
        self.dir = 'csvs/' + prefix + '/'
 
    def save_csv(self, rep):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        np.savetxt(self.dir + self.name + '.csv', rep, delimiter=',')

        