import math
import random
import numpy as np
import operator
from copy import deepcopy

class Point:
    def __init__(self, position , fitness , corr):
        self.position = position
        self.fitness = fitness
        self.corr = corr

class Particle:
    def __init__(self, position , fitness , corr):
        self.current = Point(position , fitness , corr)
        self.new = deepcopy(self.current)
        self.stdiv = 0.1
        self.c = 0 


class ncs:
    def __init__(self,func,min_bound,max_bound,dimension,n_point,iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.swarms = self.init_swarm()
        self.globle_point = deepcopy(self.swarms[0].current)
        self.r = 0.99
        self.epoch = 10

    def init_swarm(self):
        swarms = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound,self.dimension)
            fitness = self.func(position)
            corr = float("inf") 
            swarms.append(Particle( position , fitness , corr))
        swarms = sorted(swarms, key= operator.attrgetter('new.fitness'))
        return swarms  

    def move_swarm(self):

        for iter in range(self.iteration):
            # (8)
            mean, standard_deviation = 1, 0.1 - 0.1 * (iter / self.iteration) # mean and standard deviation
            lambda_t = np.random.normal(mean, standard_deviation)

            for i in range(self.n_point):
                # line 8
                self.swarms[i].new.position = deepcopy(self.swarms[i].current.position + np.random.normal(0 , self.swarms[i].stdiv))
                # check upper and lower bound
                for j in range(self.dimension):
                    if self.swarms[i].new.position[j] > self.max_bound:
                        self.swarms[i].new.position[j] = self.max_bound
                    if self.swarms[i].new.position[j] < self.min_bound:
                        self.swarms[i].new.position[j] = self.min_bound
                # line 9            
                self.swarms[i].new.fitness = self.func(self.swarms[i].new.position)
                
                # pseudo-code line 12 - 13
                if self.swarms[i].new.fitness < self.globle_point.fitness:
                    self.globle_point = deepcopy(self.swarms[i].new)
                
                self.Curresponding()
                
            for i in range(self.n_point):
                # pseudo-code line 15 - 16
                if lambda_t > (self.swarms[i].new.fitness / self.swarms[i].new.corr):
                    self.swarms[i].current.position = deepcopy(self.swarms[i].new.position)
                    self.swarms[i].c += 1

        #     # 20 - 22
            if iter % self.epoch == 0:
                for i in range(self.n_point):
                    if (self.swarms[i].c / self.epoch) > 0.2:
                        self.swarms[i].stdiv = self.swarms[i].stdiv / self.r
                    elif (self.swarms[i].c / self.epoch) < 0.2:
                        self.swarms[i].stdiv = self.swarms[i].stdiv * self.r
                    self.swarms[i].c = 0

            print iter , self.globle_point.fitness
        print np.array(self.globle_point.position)


    def Curresponding(self):
        for i in range(self.n_point):
            for j in range(self.n_point):
                if j is not i :
                    D = sum(((self.swarms[i].current.position - self.swarms[j].current.position)**2) / (((self.swarms[i].stdiv **2) + self.swarms[j].stdiv**2)/2)) 
                    D = D/8 + math.log(math.pow((self.swarms[i].stdiv**2 + self.swarms[j].stdiv**2)/2 , 2 * self.dimension)/ math.sqrt(math.pow(self.swarms[i].stdiv**2 , 2*self.dimension) * math.pow(self.swarms[j].stdiv**2 , 2*self.dimension)))/2
                    if D < self.swarms[i].current.corr:
                        self.swarms[i].current.corr = D
                    D = 0
                    D = sum(((self.swarms[i].new.position - self.swarms[j].current.position)**2) / (((self.swarms[i].stdiv **2) + self.swarms[j].stdiv**2)/2)) 
                    D = D/8 + math.log(math.pow((self.swarms[i].stdiv**2 + self.swarms[j].stdiv**2)/2 , 2 * self.dimension)/ math.sqrt(math.pow(self.swarms[i].stdiv**2 , 2*self.dimension) * math.pow(self.swarms[j].stdiv**2 , 2*self.dimension)))/2
                    if D < self.swarms[i].new.corr:
                        self.swarms[i].new.corr = D
