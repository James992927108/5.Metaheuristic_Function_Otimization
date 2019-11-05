from __future__ import division

import math

import numpy as np


class cec05:
    def __init__(self, func_num, dimension):
        np.set_printoptions(precision=6, suppress=False)
        self.dim = dimension
        self.func_num = func_num
        if self.dim != 10 and self.dim != 30 and self.dim != 50 and self.dim != 100:
            print "\nError: Test functions are only defined for D=10,30,50,100.\n"
        # Load shift_data
        if self.func_num != 0:
            self.OShift = np.array(self.loadShiftData(func_num))
            
            if self.func_num == 3:
                self.M = np.array(self.loadRotateData(func_num))
            else:
                self.M = np.zeros(self.dim)
        
    def func(self, x):
        """x is position """
        f = self.func_map(str(self.func_num))(x)
        return f

    def func_map(self, func_num):
        return {
            '0': self.rosenbrock,
            '1': self.Shifted_Sphere_Function,
            '2': self.Shifted_Schwefel_Problem_1_2,
            '3': self.Shifted_Rotated_High_Conditioned_Elliptic_Function,
            '4': self.Shifted_Schwefel_Problem_1_2_with_Noise_in_Fitness,
            # '5': self.COP_05,
        }.get(func_num, 'nothing') 

    def getFunctionDetails(self, func_num):
        # [lb, ub]
        return {
            0: [-30, 30],
            1: [-100, 100],
            2: [-100, 100],
            3: [-100, 100],
            4: [-100, 100],
        }.get(func_num, "nothing")
    # ------------------------------------------------------------------
    # For test F0
    def rosenbrock(self, x):
        sum = 0
        for i in range(self.dim -1):
            sum = sum + 100 * (x[i+1] - (x[i])**2)**2 + (x[i] -1)**2
        return sum

    # F1
    def Shifted_Sphere_Function(self, x):
        r_flag = 0
        f_bias = -450.0
        z = self.sr_func(x, r_flag)
        f = sum(z**2) + f_bias
        return f
    # F2
    def Shifted_Schwefel_Problem_1_2(self, x):
        r_flag = 0
        f_bias = -450.0
        z = self.sr_func(x, r_flag)
        f = 0.0
        for i in range(self.dim):
            t = 0.0
            for j in range(i):
                t += z[j]
            f += t**2
        f += f_bias
        return f
    # F3
    def Shifted_Rotated_High_Conditioned_Elliptic_Function(self, x):
        r_flag = 1
        f_bias = -450.0
        z = self.sr_func(x , r_flag)
        f = 0.0
        for i in range(1,self.dim):
            power = (i - 1) / (self.dim - 1)
            f += math.pow(10**6 , power) * (z[i]**2)
        f += f_bias
        return f
    # F4   
    def Shifted_Schwefel_Problem_1_2_with_Noise_in_Fitness(self, x):
        r_flag = 0
        f_bias = -450.0
        z = self.sr_func(x , r_flag)
        f = 0.0
        part1 = 0.0
        for i in range(self.dim):
            t = 0.0
            for j in range(i):
                t += z[j]
            part1 += t**2
        f = part1 * (1 + 0.4 * abs(np.random.normal(0,1))) + f_bias
        return f
        
    # ------------------------------------------------------------------
    def sr_func(self, x, r_flag):
        if r_flag == 0:
            sr_x = self.shiftfunc(x, self.OShift)            
        elif r_flag == 1:
            y = self.shiftfunc(x, self.OShift)
            sr_x = self.rotatefunc(y, self.M)
        return sr_x

    def shiftfunc(self, x, OShift):
        xshift = x - OShift
        return xshift

    def rotatefunc(self, y, M):
        xrot = np.dot(y , M)
        return xrot

    def loadShiftData(self, func_num):
        FileName = self.getloadShiftDataFileName(func_num)
        data = np.array([x for x in open(FileName).read().split()]).astype(np.float)
        pV = []        
        for i in range(self.dim):
            pV.append(data[i])
        return pV

    def getloadShiftDataFileName(self, func_num):
        return {  
            1: "benchmarks/cec05/inputData/sphere_func_data.txt",
            2: "benchmarks/cec05/inputData/schwefel_102_data.txt",
            3: "benchmarks/cec05/inputData/high_cond_elliptic_rot_data.txt",
            4: "benchmarks/cec05/inputData/schwefel_102_data.txt",
        }.get(func_num, "nothing")
    
    def loadRotateData(self, func_num):
        FileName = self.getloadRotateDataFileName(func_num)
        data = np.loadtxt(FileName)
        return data

    def getloadRotateDataFileName(self, func_num):
        return {  
            3: "benchmarks/cec05/inputData/elliptic_M_D{}.txt".format(self.dim),
        }.get(func_num, "nothing")

if __name__ == "__main__":

    dimension = 10
    func_num = 4
    print func_num
    cec = cec05(func_num, dimension)

    x = np.array(cec.loadShiftData(func_num))
    print np.array(x)
    print cec.func(x)

    min_bound , max_bound = cec.getFunctionDetails(func_num)
    x = np.random.uniform(min_bound , max_bound , dimension)
    print np.array(x)
    print cec.func(x)
