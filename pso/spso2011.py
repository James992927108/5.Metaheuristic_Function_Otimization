# Source Generated with Decompyle++
# File: SPSO2011.cpython-34.pyc (Python 3.4)

from copy import deepcopy
from operator import attrgetter
import numpy as np


class Point:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position


class Particle:
    def __init__(self, position, velocity):
        self.current = Point(np.finfo(np.float32).max, position)
        self.velocity = velocity
        self.previous_best = deepcopy(self.current)
        self.previous_best_neighbor = deepcopy(self.current)


class spso2011:
    def __init__(self, func, min_bound, max_bound,dimension, n_point, iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.w = 1.0 / (2.0 * np.log(2.0))
        self.c = 0.5 + np.log(2.0)

        self.topology = self.random_topology(K=3)
        
        self.best_point = Point(np.finfo(np.float32).max, np.random.randint(
            self.min_bound, self.max_bound, self.dimension))
        self.convergence_list = np.zeros(self.iteration)

        self.swarm = self.init_swarm()

    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = [np.random.uniform(self.min_bound, self.max_bound)
                 for d in range(self.dimension)]

            velocity = [np.random.uniform(self.min_bound - position[d], self.max_bound - position[d])
                 for d in range(self.dimension)]

            swarm.append(Particle(np.array(position), np.array(velocity)))

        return swarm

    def random_topology(self, K=3):
        A = np.eye(self.n_point)
        v = np.random.randint(self.n_point, size=(self.n_point, K))
        for i in range(v.shape[0]):
            A[i, v[i]] = 1

        topology = [[] for i in range(self.n_point)]
        for (i, j) in np.argwhere(A > 0):
            topology[j].append(i)

        return np.array(topology)

    def move_swarm(self):
        for iter in range(self.iteration):
            # self.w = 0.5 - (0.5- 0.1) * iter / self.iterationf
            for i in np.random.permutation(self.n_point):

                p = self.swarm[i]

                # Update best of previous_best in neighborhood
                best_neighbor = min([self.swarm[neighbor] for neighbor in self.topology[i]],
                                    key=attrgetter('previous_best.fitness'))
                p.previous_best_neighbor = deepcopy(best_neighbor.previous_best)

                # Update velocity
                random_position = self.sample_from_hypersphere(p)
                p.velocity = self.w * p.velocity + random_position - p.current.position

                # Update position
                p.current.position += p.velocity

                self.check_confinement(i)

                # Update previous_best
                p.current.fitness = self.func(p.current.position)
                if p.current.fitness < p.previous_best.fitness:
                    p.previous_best = deepcopy(p.current)

                    # Update best of previous_best in neighborhood
                    if p.previous_best.fitness < p.previous_best_neighbor.fitness:
                        p.previous_best_neighbor = deepcopy(p.previous_best)

                best = min(self.swarm, key=attrgetter('current.fitness'))

                # Update topology if the best know solution has not been improved
                if best.current.fitness >= self.best_point.fitness:
                    self.topology = self.random_topology()
                    self.best_point = deepcopy(self.best_point)
                else:
                    self.best_point = deepcopy(best.current)

            self.convergence_list[iter] = self.best_point.fitness
            # print iter , self.best_point.fitness
        return self.convergence_list , self.best_point

    def sample_from_hypersphere(self, particle):

        x = particle.current.position
        p = particle.previous_best.position
        l = particle.previous_best_neighbor.position

        if (l != p).any():
            centre = x + (self.c / 3.0) * (p + l - 2.0 * x)
        else:
            centre = x + (self.c / 2.0) * (p - x)

        r_max = np.linalg.norm(centre - x)
        r = np.random.uniform(0.0, r_max)
        v = np.random.uniform(0.0, 1.0, size=self.dimension)
        v = v * (r / np.linalg.norm(v))

        return centre + v

    def check_confinement(self, index):
        p = self.swarm[index]

        min_index = np.where(p.current.position < self.min_bound)
        max_index = np.where(p.current.position > self.max_bound)

        if min_index:
            p.current.position[min_index] = np.random.uniform(self.min_bound , self.max_bound)
            p.velocity[min_index] = np.random.uniform(self.min_bound , self.max_bound)

        if max_index:
            p.current.position[max_index] = np.random.uniform(self.min_bound , self.max_bound)
            p.velocity[max_index] = np.random.uniform(self.min_bound , self.max_bound)
 