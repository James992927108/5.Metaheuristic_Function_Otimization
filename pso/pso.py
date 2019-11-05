import random
import math
import numpy as np


class Particle:
    def __init__(self, position, velocity):
        self.position = []          # particle position
        self.velocity = []          # particle velocity
        self.best_position = []          # best position individual
        self.best_fitness = -1          # best error individual
        self.fitnesses = -1               # error individual

        for i in range(len(position)):
            self.velocity.append(velocity[i])
            self.position.append(position[i])

class pso():
    def __init__(self, func, min_bound, max_bound,dimension, n_point, iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.w = 1.0 / (2.0 * np.log(2.0))
        self.c1 = 0.5 + np.log(2.0)
        self.c2 = 0.5 + np.log(2.0)

        self.global_fitness = -1                   # best error for group
        self.global_position = []                   # best position for group
        self.global_fitness_array = np.zeros(self.iteration)

        self.swarm = self.init_swarm()

    def init_swarm(self):
        swarm = []
        for i in range(0, self.n_point):
            position = np.random.randint(
                self.min_bound, self.max_bound, self.dimension)
            velocity = np.random.uniform(
                self.min_bound, self.max_bound, self.dimension)
            swarm.append(Particle(position, velocity))
        return swarm

    def move_swarm(self):
        for iter in range(self.iteration):

            self.w = 0.5 - (0.5 - 0.1) * iter / self.iteration
            for i in range(self.n_point):
                p = self.swarm[i]
                p.fitnesses = self.func(p.position)

                if p.fitnesses < p.best_fitness or p.best_fitness == -1:
                    p.best_position = p.position
                    p.best_fitness = p.fitnesses

                if p.fitnesses < self.global_fitness or self.global_fitness == -1:
                    self.global_position = list(p.position)
                    self.global_fitness = float(p.fitnesses)

            for i in range(self.n_point):
                p = self.swarm[i]

                # self.swarm[j].update_velocity(self.gloab_position)
                for j in range(self.dimension):
                    r1 = random.random()
                    r2 = random.random()

                    vel_cognitive = self.c1*r1 * (p.best_position[j] - p.position[j])
                    vel_social = self.c2*r2 * (self.global_position[j]-p.position[j])
                    p.velocity[j] = self.w * p.velocity[j]+vel_cognitive+vel_social

                # p.update_position(self.min_bound, self.max_bound)
                for j in range(self.dimension):
                    p.position[j] = p.position[j] + p.velocity[j]
                    # adjust maximum position if necessary
                    if p.position[j] > self.max_bound:
                        p.position[j] = np.random.uniform(self.min_bound , self.max_bound)
                        p.velocity[j] = np.random.uniform(self.min_bound , self.max_bound)
                    # adjust minimum position if neseccary
                    if p.position[j] < self.min_bound:
                        p.position[j] = np.random.uniform(self.min_bound , self.max_bound)
                        p.velocity[j] = np.random.uniform(self.min_bound , self.max_bound)
            
            # self.global_fitness_array[iter] = self.global_fitness
            print iter ,  self.global_fitness
        return np.array(self.global_fitness_array)
