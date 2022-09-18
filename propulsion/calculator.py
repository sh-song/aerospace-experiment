import math
import numpy as np
class Calculator:
    def __init__(self, prefix, trt, rep_num, data, target):
        self.target = target
        self.name = prefix + '-' + trt +'-' +rep_num
        self.dir = 'figures/' + prefix + '/'
        self.raw = data
        self.filtered_data = None

        self.Astar = math.pi * (0.002 ** 2) 
        self.T = 300.0
        self.gamma = 1.395 #specific heat ratio
        self.R = 0.2598 #gas constant
        self.M = 2.94


    def calc_mdot(self, input):

        P = input
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

    def run(self, input):
        if self.target == "mdot":
            return self.calc_mdot(input)

        elif self.target == "exit_pressure":
            return self.exit_pressure(input)
        