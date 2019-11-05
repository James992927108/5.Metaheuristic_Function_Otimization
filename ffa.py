import random
import numpy as np
from copy import deepcopy
import math


class Agent:
    def __init__(self, position, fitness):
        """fitness = fitness"""
        self.fitness = fitness
        self.position = position


class ffa:
    def __init__(self, func, min_bound, max_bound, dimension, n_point, iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.gamma = 1
        self.alpha = 0.2
        # self.gamma = np.random.uniform(0.01, 100)
        # self.alpha = random.random()
        self.swarm = self.init_swarm()

        self.globle = Agent(np.zeros(self.dimension) , float("inf"))

    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound, self.dimension)
            fitness = self.func(position)
            swarm.append(Agent(position, fitness))
        return swarm

    def move_swarm(self):
        for iter in range(self.iteration):
            """ update """
            for i in range(self.n_point):
                for j in range(self.n_point):
                    if self.swarm[j].fitness > self.swarm[i].fitness:
                        # (9)
                        self.swarm[i].position += math.exp((-self.gamma) * (np.linalg.norm(self.swarm[j].position - self.swarm[i].position)**2)) * (
                            self.swarm[j].position - self.swarm[i].position) + self.alpha*(random.random()*0.5)
                            
                """check upper and lower bound"""
                self.swarm[i].position[self.swarm[i].position > self.max_bound] =  np.random.uniform(self.min_bound , self.max_bound)
                self.swarm[i].position[self.swarm[i].position < self.min_bound] =  np.random.uniform(self.min_bound , self.max_bound)
                
                self.swarm[i].fitness = self.func(self.swarm[i].position)
                if self.swarm[i].fitness  < self.globle.fitness:
                    self.globle = deepcopy(self.swarm[i])

            print iter , self.globle.fitness
        # print np.array(self.globle.position)
        print self.globle.fitness
        return self.globle  
