import random
from copy import deepcopy
import math
import numpy as np

class Agent:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class goa:
    def __init__(self,func,min_bound,max_bound,dimension,n_point,iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.cMax = 0.1
        self.cMin = 0.00004
        self.l = 1.5
        self.f = 0.5

        self.global_point = Agent(np.finfo(np.float32).max ,  np.random.uniform(self.min_bound, self.max_bound,self.dimension))
        self.swarm = self.init_swarm()
        self.global_fitness_array=np.zeros(self.iteration)

    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound,self.dimension)
            swarm.append(Agent(np.finfo(np.float32).max, position))
        return swarm     

    # kernprof -l -v run.py  

    # @profile
    def move_swarm(self):
        for iter in range(self.iteration):
            # (2.8)            
            """ use grey wolf optimization """
            c = self.cMax - (iter * ((self.cMax - self.cMin) / self.iteration))              
            for i in range(self.n_point):
                # (2.7)
                for j in range(self.dimension):
                    self.swarm[i].position[j] = c * self.get_xi(i , c , j)  + self.global_point.position[j]

            for i in range(self.n_point):   
                for j in range(self.dimension):
                    if(self.swarm[i].position[j]  > self.max_bound or self.swarm[i].position[j]  < self.min_bound):
                        self.swarm[i].position[j]  = np.random.uniform(self.min_bound, self.max_bound)
        
            for i in range(self.n_point):            
                self.swarm[i].fitness = self.func(self.swarm[i].position)
                if self.swarm[i].fitness < self.global_point.fitness:
                    self.global_point = deepcopy(self.swarm[i])

            # self.global_fitness_array[iter]= self.global_point.fitness
            # print np.array(self.global_fitness_array)
            # print np.array(self.global_point.position)
            print iter ,  self.global_point.fitness
        return self.global_point
        
    # @profile     
    def get_xi(self , i , c , j):
        temp = 0
        for point in range(self.n_point):
            if point != i:    
                r = math.sqrt((self.swarm[point].position[j] - self.swarm[i].position[j])**2)
                if r == 0:
                    r = 1
                r = (self.swarm[point].position[j] - self.swarm[i].position[j]) / r
                temp += c * ((self.max_bound - self.min_bound) / 2) * self.s_fun(r) * r  
        return temp
 
    # (2.3)
    # @profile
    def s_fun(self , r):
        part1 = self.f * math.exp((-r) / self.l)
        part2 = math.exp(-r)
        return part1 - part2
