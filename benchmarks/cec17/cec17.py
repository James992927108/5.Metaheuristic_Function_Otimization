import numpy as np
import math
# table = [
#     {'COP': 1,'r_flag': 0},
#     {'COP': 2,'r_flag': 1},
#     {'COP': 3,'r_flag': 0},
#     {'COP': 4,'r_flag': 0},
#     {'COP': 5,'r_flag': 1},
#     {'COP': 6,'r_flag': 0},
#     {'COP': 7,'r_flag': 0},
#     {'COP': 8,'r_flag': 0},
#     {'COP': 9,'r_flag': 0},
#     {'COP': 10,'r_flag': 0},
#     {'COP': 11,'r_flag': 0},
#     {'COP': 12,'r_flag': 0},
#     {'COP': 13,'r_flag': 0},
#     {'COP': 14,'r_flag': 0},
#     {'COP': 15,'r_flag': 0},
#     {'COP': 16,'r_flag': 0},
#     {'COP': 17,'r_flag': 0},
#     {'COP': 18,'r_flag': 0},
#     {'COP': 19,'r_flag': 0},
#     {'COP': 20,'r_flag': 0},
#     {'COP': 21,'r_flag': 1},
#     {'COP': 22,'r_flag': 1},
#     {'COP': 23,'r_flag': 1},
#     {'COP': 24,'r_flag': 1},
#     {'COP': 25,'r_flag': 1},
#     {'COP': 26,'r_flag': 1},
#     {'COP': 27,'r_flag': 1},
#     {'COP': 28,'r_flag': 1},
# ]
# TODO can use zip tp set up the function

class cec17:
    def __init__(self, func_num, dimension):
        self.dim = dimension
        self.func_num = func_num

        if self.dim != 10 and self.dim != 30 and self.dim != 50 and self.dim != 100:
            print "\nError: Test functions are only defined for D=10,30,50,100.\n"
        # Load shift_data
        self.OShift = np.array(self.loadShiftData(func_num))
        # Load Matrix M
        if func_num == 2 or func_num > 20:
            self.M = np.array(self.loadRotateData(func_num, 0))
        else:
            self.M = np.zeros(self.dim)
        if func_num == 5:
            self.M1 = self.loadRotateData(func_num, 1)
            self.M2 = self.loadRotateData(func_num, 2)

    def func(self, x):
        """x is position """
        f, g, h = self.func_map(str(self.func_num))(x)
        return f

    def func_map(self, func_num):
        return {
            '1': self.COP_01,
            '2': self.COP_02,
            # '3': self.COP_01,
            # '4': self.COP_01,
            '5': self.COP_05,
        }.get(func_num, 'test')
# ---------------------------------------------------------------------------------------
    def COP_01(self, x):
        r_flag = 0
        z = self.sr_func(x, self.OShift, self.M, r_flag)
        f = 0.0
        for i in range(self.dim):
            t = 0.0
            for j in range(i):
                t += z[j]
            f += t*t
        g = 0.0
        for i in range(self.dim):
            g += z[i] * z[i] - 5000 * math.cos(0.1*math.pi*z[i]) - 4000
        h = 0
        return f, g, h

    def COP_02(self, x):
        # only here r_flag = 1 is different with COP01
        r_flag = 1
        z = self.sr_func(x, self.OShift, self.M, r_flag)
        f = 0.0
        for i in range(self.dim):
            t = 0.0
            for j in range(i):
                t += z[j]
            f += t*t
        g = 0.0
        for i in range(self.dim):
            g += z[i] * z[i] - 5000 * math.cos(0.1*math.pi*z[i]) - 4000
        h = 0
        return f, g, h
    
    def COP_05(self, x):
        r_flag = 1
        z = self.sr_func(x, self.OShift, self.M, 0)
        z1 = self.sr_func(x, self.OShift, self.M1, r_flag)
        z2 = self.sr_func(x, self.OShift, self.M2, r_flag)
        f = 0.0
        for i in range(self.dim - 1):
            f += (100 *(z[i]**2 - z[i+1])**2 + (z[i] - 1) **2)
        
        g = np.zeros(2)
        for i in range(self.dim):
            g[0] += z1[i]**2 - 50 * math.cos(2 * math.pi *z1[i]) - 40
        for i in range(self.dim):
            g[1] += z2[i]**2 - 50 * math.cos(2 * math.pi *z2[i]) - 40
        h = 0
        return f, g , h
# ------------------------------------------------------------------
    def sr_func(self, x, Os, Mr, r_flag):
        if r_flag == 1:
            y = self.shiftfunc(x, Os)
            sr_x = self.rotatefunc(y, Mr)
        else:
            sr_x = self.shiftfunc(x, Os)
        return sr_x

    def shiftfunc(self, x, Os):
        xshift = np.zeros(self.dim)
        for i in range(self.dim):
            xshift[i] = x[i] - Os[i]
        return xshift

    def rotatefunc(self, y, Mr):
        xrot = np.zeros(self.dim **2)
        for i in range(self.dim):
            for j in range(self.dim):
                xrot[i] += y[j] * np.float(Mr[i * self.dim + j])
        return xrot

    def loadShiftData(self, func_num):
        pV = []
        FileName = "inputData/shift_data_{}.txt".format(func_num)
        data = np.array([x for x in open(FileName).read().split()]).astype(np.float)
        for i in range(self.dim):
            pV.append(data[i])
        return pV

    def loadRotateData(self, func_num, f5_flag):
        pM = []
        if func_num == 5:
            FileName = "inputData/M{}_{}_D{}.txt".format(
                f5_flag, func_num, self.dim)
        else:
            FileName = "inputData/M_{}_D{}.txt".format(func_num, self.dim)

        data = np.array([x for x in open(FileName).read().split()])
        for i in range(self.dim **2):
            pM.append(data[i])
        return pM

if __name__ == "__main__":
    """
    dim = dimension
    x = position (1-dimension)
    dim = len(x)
    # inputData/
    """
    dimension = 10
    # x = np.random.uniform(-1, 1, dimension)
    func_num = 1
    cec = cec17(func_num, dimension)
    """get the best x position"""
    x = np.array(cec.loadShiftData(func_num))
    print np.array(x)
    print cec.func(x)

    x = np.random.uniform(-100, 100, dimension)
    print np.array(x)
    print cec.func(x)