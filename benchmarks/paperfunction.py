from __future__ import division

import math

import numpy as np

class paperfunction:
    def __init__(self, func_num, dimension):
        np.set_printoptions(precision=6, suppress=False)
        self.dim = dimension
        self.func_num = func_num
        if self.dim != 10 and self.dim != 30 and self.dim != 50 and self.dim != 100:
            print "\nError: Test functions are only defined for D=10,30,50,100.\n"
        
    def func(self, x):
        """x is position """
        f = self.func_map(str(self.func_num))(x)
        return f

    def func_map(self, func_num):
        return {
            '1': self.F1,
            '2': self.F2,
            '3': self.F3,
            '4': self.F4,
            '5': self.F5,
            '6': self.F6,
            '7': self.F7,

        }.get(func_num, 'nothing') 

    def getFunctionDetails(self, func_num):
        # [lb, ub]
        return {  
            1: [-100, 100],
            2: [-10, 10],
            3: [-100, 100],
            4: [-100, 100],
            5: [-30, 30],
            6: [-100, 100],
            7: [-1.28, 1.28],
        }.get(func_num, "nothing")
    # ------------------------------------------------------------------
    # F1
    def F1(self, x):
        f = sum(x**2)
        return f
    # F2
    def F2(self, x):
        f = 0.0
        part1 = 0.0
        part2 = 0.0
        for i in range(self.dim):
            part1 += abs(x[i])
            part2 *= abs(x[i])
        f = part1 + part2
        return f
    # F3
    def F3(self, x):
        f = 0.0
        for i in range(self.dim):
            t = 0.0
            for j in range(i):
                t += x[j]
            f += t**2
        return f
    # F4   
    def F4(self, x):
        f = 0
        return f
    # F5   
    def F5(self, x):
        f = 0
        for i in range(self.dim - 1):
            part1 = 100 * (x[i+1] - x[i]**2)**2
            part2 = (x[i]-1)**2
            f += (part1 + part2)
        return f
    # F6   
    def F6(self, x):
        f = 0
        for i in range(self.dim):
            f += (x[i] + 0.5)**2
        return f
    # F7   
    def F7(self, x):
        f = 0
        for i in range(self.dim):
            f += i*(x[i]**4)
        f += np.random.uniform(0,1)
        return f
        
    # ------------------------------------------------------------------

if __name__ == "__main__":

    dimension = 30
    func_num = 7
    print func_num
    p_fun = paperfunction(func_num, dimension)

    min_bound , max_bound = p_fun.getFunctionDetails(func_num)
    x = np.random.uniform(min_bound , max_bound , dimension)
    print np.array(x)
    print p_fun.func(x)
