import math
import random
import numpy as np
import operator
from copy import deepcopy 


class Agent():
    def __init__(self,fitness,position):
        self.fitness = fitness
        self.position = position
class mbo():
    def __init__(self,func,min_bound,max_bound,dimension,n_point,iteration):

        self.func = func
        self.min_bounds = min_bound
        self.max_bounds = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration


        self.maxt = 50
        # note : can set p as big as posible at first , and decreased the p when iteration increases
        self.p = 5.0 / 12 
        self.peri = 1.2
        self.BAR = self.p
        self.keep = 5

        self.numButterfly1 = int(math.ceil(self.n_point * self.p))
        self.numButterfly2 = self.n_point - self.numButterfly1
        
        self.global_Agent = Agent(np.finfo(np.float32).max, np.random.uniform(self.min_bounds, self.max_bounds,self.dimension))
        self.Smax = 1.0

        self.init_swarm()
        self.init_rand1_land2_elitism()
        
    def init_swarm(self):
        self.swarms = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bounds, self.max_bounds,self.dimension)
            self.swarms.append(Agent( 0 , position))

    def init_rand1_land2_elitism(self):
        self.land1 = []
        self.land2 = []
        self.elitism = []
        for i in range(self.numButterfly1):
            self.land1.append(self.swarms[i])
        for i in range(self.numButterfly1 , self.n_point):
            self.land2.append(self.swarms[i])
        for i in range(self.keep):
            self.elitism.append(self.swarms[i])
        
    def move_swarm(self):
        for iter in range(self.iteration):
            self.divide_swarm_into_land1_land2()
            # migration operator
            for j in range(self.numButterfly1):
                r = random.random() * self.peri 
                for k in range(self.dimension):
                    # (2)
                    if  r <= self.p:
                        r1 = np.random.randint(0, self.numButterfly1)
                        # (1)
                        self.swarms[j].position[k] = self.land1[r1].position[k]
                    else:
                        r2 = np.random.randint(0, self.numButterfly2)
                        # (3)
                        self.swarms[j].position[k] = self.land2[r2].position[k]

            # Butterfly adjusting operator
            for j in range(self.numButterfly2):
                # (7)
                StepSize = int(math.ceil(self.exprnd(2 * self.maxt)))
                delataX = self.LevyFlight(StepSize)
                # (8)
                if iter == 0 :
                    scale = self.Smax / math.pow(1, 2)
                else:
                    scale = self.Smax / math.pow(iter, 2)

                r = random.random()
                for k in range(self.dimension):
                    if r <= self.p:
                        # (4)
                        self.swarms[self.numButterfly1 + j].position[k] = self.global_Agent.position[k]
                    else:
                        # (5)
                        r3 = np.random.randint(0, self.numButterfly2)
                        self.swarms[self.numButterfly1 + j].position[k] = self.land2[r3].position[k]

                        if random.random() > self.BAR:
                            # (6)
                            self.swarms[self.numButterfly1 + j].position[k] += scale * (delataX[k] - 0.5)

            self.checkupperandlower()

            for j in range(self.n_point):
                self.swarms[j].fitness = self.func(np.array(self.swarms[j].position))
                if self.swarms[j].fitness < self.global_Agent.fitness:
                    self.global_Agent = deepcopy(self.swarms[j])
            # sort swarms according to fitness
            self.swarms = sorted(self.swarms, key= operator.attrgetter('fitness'))
            # replace the worst
            self.replace_worst()
            # keep current two best , use in next iteration 
            self.keep_current()
            
        #     print iter, self.global_Agent.fitness
        # print self.global_Agent.position
        print self.global_Agent.fitness

    def print_bug(self):
        print "------------"
        for i in range(self.n_point):
            print i , self.swarms[i].fitness
        print "@@@@@@@@@@@@"
        for i in range(len(self.elitism)):
            print i , self.elitism[i].fitness

    def divide_swarm_into_land1_land2(self):
        for i in range(self.numButterfly1):
            self.land1[i] = deepcopy(self.swarms[i])
        for i in range(self.numButterfly2):
            self.land2[i] = deepcopy(self.swarms[self.numButterfly1 + i])

    def checkupperandlower(self):
        for i in range(self.n_point):
            for j in range(self.dimension):
                if self.swarms[i].position[j] > self.max_bounds:
                    self.swarms[i].position[j] = self.max_bounds
                if self.swarms[i].position[j] < self.min_bounds:
                    self.swarms[i].position[j] = self.min_bounds

    def exprnd(self, mu):
        return -1.0 / mu * math.log(1 - random.random())

    def LevyFlight(self, StepSize):
        delataX = []
        fx = []
        for i in range(self.dimension):
            for j in range(StepSize):
                fx.append(math.tan(math.pi * random.random()))
            delataX.append(sum(fx))
        return delataX
        
    def replace_worst(self):
        for i in range(self.keep):
            self.swarms[self.n_point - i - 1] = deepcopy(self.elitism[i])

    def keep_current(self):
        self.elitism[:] = []
        for i in range(self.keep):
            self.elitism.append(self.swarms[i])
