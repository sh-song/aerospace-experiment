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

        #2-1
        self.T_e = self.calc_T_e()
        self.V_e = 589.2
        # self.V_e = self.calc_V_e()
        self.P_b = 1 #bar
        self.A_e = 4 * self.Astar
        

    def calc_T_e(self):
        a = (self.gamma - 1) / 2
        b = 1 + a*(self.M**2)
        output = self.T / b
        print(f"T_e: {output}")
        return output
    def calc_V_e(self):
        a = self.gamma * self.R * self.T_e
        b = math.sqrt(a)
        output = self.M * b
        print(f"V_e: {output}")
        return output
 
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
        return a*b*(c**d) * 1000 #kg to g

    def calc_exit_pressure(self, input):
        
        gamma = self.gamma
        M = self.M

        a = (gamma + 1) / 2
        b = 1 + a*(M**2)
        c = - gamma / (gamma - 1)
        return input*(b**c)

    def calc_thrust(self, mdot, P_e):
        mdot = mdot
        V_e = self.V_e
        P_e = P_e
        P_b = self.P_b
        A_e = self.A_e
        
        a = mdot*V_e
        b = (P_e - P_b) * A_e
        return a + b

    def run(self, target):
        if target == "mdot":
            print('calculate mdot')
            output = np.zeros(self.input.shape)
            output[:, 0] = self.input[:, 0].copy()
            for i, P in enumerate(self.input[:, 2]):
                output[i, 1] = self.calc_mdot(P)
            return output

        elif target == "exit_pressure":
            print('calculate P_e')
            output = np.zeros(self.input.shape)
            output[:, 0] = self.input[:, 0].copy()
            for i, P in enumerate(self.input[:, 2]):
                output[i, 1] = self.calc_exit_pressure(P) 
            return output

        elif target == "thrust":
            output = np.zeros(self.input.shape)
            output[:, 0] = self.input[:, 0].copy()
            for i, vec in enumerate(self.input):
                output[i, 1] = self.calc_thrust(vec[1], vec[2]) #mdot, P_e
            return output


        
