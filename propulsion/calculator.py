import math
import numpy as np
class Calculator:
    def __init__(self, prefix, trt, rep_num, input):
        self.name = prefix + '-' + trt +'-' +rep_num
        self.dir = 'figures/' + prefix + '/'
        self.input = input

        self.Astar = math.pi * (0.002 ** 2) 
        self.T = 300.0
        self.gamma = 1.395 #specific heat ratio
        self.R = 0.2598 #gas constant
        self.M = 2.94


    def calc_mdot(self, P):

        P = P
        Astar = self.Astar
        T = self.T
        gamma = self.gamma
        R = self.R

        a = Astar * P / math.sqrt(T)
        b = math.sqrt(gamma / R)
        c = (gamma + 1) / 2
        d = -(gamma + 1) / (2*gamma - 2)
        return a*b*(c**d)

    def calc_exit_pressure(self, input):
        
        gamma = self.gamma
        M = self.M

        a = (gamma + 1) / 2
        b = 1 + a*(M**2)
        c = - gamma / (gamma - 1)
        return input*(b**c)

    def run(self, target):
        if target == "mdot":
            output = np.zeros(self.input.shape)
            output[:, 0] = self.input[:, 0]
            for i, P in enumerate(self.input[:, 2]):
                output[i, 1] = self.calc_mdot(P) 
            return output

        elif target == "exit_pressure":
            output = np.zeros(self.input.shape)
            output[:, 0] = self.input[:, 0]
            for i, P in enumerate(self.input[:, 2]):
                output[i, 1] = self.calc_exit_pressure(P) 
            return output


        