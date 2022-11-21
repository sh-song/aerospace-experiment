import math
import numpy as np
class Calculator:
    def __init__(self, prefix, trt, input):
        self.name = prefix + '-' + trt
        self.dir = 'figures/' + prefix + '/'
        self.input = input

        self.theta = np.radians(float(trt))
        self.rho = 1.2
        self.V = 20
        self.S = 0.091
        self.c_bar = 0.2


    def calc_lift(self, Fx, Fy):
        return Fy*np.cos(self.theta) - Fx*np.sin(self.theta)

    def calc_lift_coeff(self, L):
        return 2*L / (self.rho * np.power(self.V, 2) * self.S)

    def calc_drag(self, Fx, Fy):
        return Fx*np.cos(self.theta) + Fy*np.sin(self.theta)

    def calc_drag_coeff(self, D):
        return 2*D / (self.rho * np.power(self.V, 2) * self.S)

    def calc_pitching_mmnt_coeff(self, M):
        return 2*M / (self.rho * np.power(self.V, 2) * self.S * self.c_bar)


    def run(self, target):
        if target == "Lift Coefficient":
            length = self.input.shape[0]
            output = np.zeros((length))
            for i in range(length):
                Fx = self.input[i][0]
                Fy = self.input[i][1]
                L = self.calc_lift(Fx, Fy)             
                output[i] = self.calc_lift_coeff(L)
            return np.mean(output)

        elif target == "Drag Coefficient":
            length = self.input.shape[0]
            output = np.zeros((length))
            for i in range(length):
                Fx = self.input[i][0]
                Fy = self.input[i][1]
                D = self.calc_drag(Fx, Fy)             
                output[i] = self.calc_drag_coeff(D)
            return np.mean(output)

        elif target == "Pitching Moment Coefficient":
            length = self.input.shape[0]
            output = np.zeros((length))
            for i in range(length):
                Mz = self.input[i][5]
                output[i] = self.calc_pitching_mmnt_coeff(Mz)
            return output