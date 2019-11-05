import random
import numpy as np
import math
import time
from copy import deepcopy



class Agent:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class woa:
    def __init__(self, func, min_bound, max_bound, dimension, n_point, iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.Leader = Agent(float("inf") , np.zeros(dimension))
        self.Positions = np.random.uniform( 0, 1, (n_point, dimension)) * (max_bound-min_bound)+min_bound


        self.convergence_curve = np.zeros(iteration)

    def move_swarm(self):

        for iter in range(self.iteration):
            for i in range(self.n_point):
                self.Positions[i, :] = np.clip(self.Positions[i, :], self.min_bound, self.max_bound)
                fitness = self.func(self.Positions[i, :])
             
                if fitness < self.Leader.fitness: 
                    self.Leader.fitness = fitness 
                    self.Leader.position = deepcopy(self.Positions[i, :])

            a = 2-iter*((2)/self.iteration)
            a2 = -1+iter*((-1)/self.iteration)

            for i in range(self.n_point):

                A = 2*a*random.random()-a  
                C = 2*random.random()   
                b = 1 
                l = (a2-1)*random.random()+1 
                p = random.random()  

                for j in range(self.dimension):
                    if p < 0.5:
                        if abs(A) >= 1:
                            rand_leader_index = int(round(math.floor(self.n_point*random.random())))
                            X_rand = self.Positions[rand_leader_index, :]
                            D_X_rand = abs(C*X_rand[j]-self.Positions[i, j])
                            self.Positions[i, j] = X_rand[j]-A*D_X_rand

                        elif abs(A) < 1:
                            # here is similar to gwo
                            D_Leader = abs(C*self.Leader.position[j]-self.Positions[i, j])
                            self.Positions[i,j] = self.Leader.position[j]-A*D_Leader

                    elif p >= 0.5:

                        distance2Leader = abs(
                            self.Leader.position[j]-self.Positions[i, j])
                        # Eq. (2.5)
                        self.Positions[i, j] = distance2Leader * math.exp(b*l)*math.cos(l*2*math.pi) + self.Leader.position[j]

            self.convergence_curve[iter] = self.Leader.fitness

            print iter , self.Leader.fitness
        print np.array(self.Leader.position)
        print self.Leader.fitness
        return self.Leader