from __future__ import division

import math
import random
from copy import deepcopy

import numpy as np
from operator import itemgetter

class Agent:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class gwo_mgoaha:
    def __init__(self, func, min_bound, max_bound, dimension, n_point, iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.l = 1.5
        self.f = 0.5
        self.Cmax = 1
        self.Cmin = 0.00001
        self.Max = 2

        self.Alpha_pos = np.zeros(self.dimension)
        self.Alpha_score = float("inf")
        self.Beta_pos = np.zeros(self.dimension)
        self.Beta_score = float("inf")
        self.Delta_pos = np.zeros(self.dimension)
        self.Delta_score = float("inf")

        self.Positions = np.random.uniform(
            0, 1, (self.n_point, self.dimension)) * (self.max_bound-self.min_bound)+self.min_bound

        self.convergence_list = np.zeros(self.iteration)

    # @profile
    def move_swarm(self):
        for iter in range(self.iteration):

            """ use grey wolf optimization """
            if iter < self.iteration * 0.75:
                a = self.Max - iter * ((self.Max)/self.iteration)
            else:
                a = self.Cmax - \
                    (iter * ((self.Cmax - self.Cmin) / self.iteration))

            for i in range(self.n_point):
                A1 = (2 * a * random.random()) - a
                C1 = 2 * random.random()
                A2 = (2 * a * random.random()) - a
                C2 = 2 * random.random()
                A3 = (2 * a * random.random()) - a
                C3 = 2 * random.random()
                # use numpy operation , so every dimension element can calculate together
                # it can imporve the proformance about 4 times.
                D_alpha = abs(C1 * self.Alpha_pos - self.Positions[i, :])
                X1 = self.Alpha_pos - A1 * D_alpha
                D_beta = abs(C2 * self.Beta_pos - self.Positions[i, :])
                X2 = self.Beta_pos - A2 * D_beta
                D_delta = abs(C3 * self.Delta_pos - self.Positions[i, :])
                X3 = self.Delta_pos - A3 * D_delta
                shift = (X1 + X2 + X3) / 3
                self.Positions[i, :] = a * self.get_xi(i, a) + shift

            for i in range(self.n_point):
                for j in range(self.dimension):
                    if(self.Positions[i, j] > self.max_bound or self.Positions[i, j] < self.min_bound):
                        self.Positions[i, j] = np.random.uniform(
                            self.min_bound, self.max_bound)

            for i in range(0, self.n_point):
                
                fitness = self.func(self.Positions[i,:])
                if fitness <= self.Alpha_score:

                    self.Alpha_score = fitness
                    for j in range(self.dimension):
                        self.Alpha_pos[j] = self.Positions[i, j]

                elif(fitness > self.Alpha_score and fitness <= self.Beta_score):
                    self.Beta_score = fitness
                    for j in range(self.dimension):
                        self.Beta_pos[j] = self.Positions[i, j]

                elif(fitness > self.Alpha_score and fitness > self.Beta_score and fitness < self.Delta_score):
                    self.Delta_score = fitness
                    for j in range(self.dimension):
                        self.Delta_pos[j] = self.Positions[i, j]


            self.convergence_list[iter] = self.Alpha_score
            # print np.array(self.convergence_list)
        return self.convergence_list, Agent(self.Alpha_score ,self.Alpha_pos)

    def get_xi(self, i, a):
        temp = np.zeros(self.dimension)
        for j in range(self.n_point):
            if j is not i:
                r = np.sqrt(
                    np.square(self.Positions[j, :] - self.Positions[i, :]))
                # r is vector , if element is 0 , i set value as 1
                r[r == 0] = 1
                r_vector = (self.Positions[j, :] - self.Positions[i, :]) / r
                temp += a * ((self.max_bound - self.min_bound) /
                             2) * self.s_fun(r) * r_vector
        return temp

    # (2.3)
    # @profile
    def s_fun(self, r):
        part1 = self.f * np.exp((-r) / self.l)
        part2 = np.exp(-r)
        return part1 - part2
