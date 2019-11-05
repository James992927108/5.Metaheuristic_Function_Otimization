
from copy import deepcopy
import numpy as np
import random
import operator

class Point:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class Particle:
    def __init__(self,position):
        self.current = Point(np.finfo(np.float32).max, position)
        self.previous_best = deepcopy(self.current)

        self.neighbors_list = []
        self.N = 0     
        self.F = 0
        self.D = 0
        self.dX = 0

class kh:
    def __init__(self , func,min_bound,max_bound,dimension,n_point,iteration):
        
        self.min_bound = min_bound
        self.max_bound = max_bound

        self.dimension = dimension
        self.n_point = n_point
        # user set paramter
        self.Nmax = 0.01
        self.Wn = random.random()
        self.tao = 1
        self.Vf = 0.02
        self.Wf = random.random()
        # Ct is a constant number between [0, 2]
        self.Ct = 1
        self.delta_t = self.get_delta_t()

        self.iteration = iteration
        self.func = func 

        # initial method have problem
        self.globe_best = Point(np.finfo(np.float32).max , np.random.uniform(self.min_bound, self.max_bound,self.dimension))
        self.globe_worst = Point(np.finfo(np.float32).min , np.random.uniform(self.min_bound, self.max_bound,self.dimension))

        self.swarm = self.init_swarm()

    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound,self.dimension)
            swarm.append(Particle(position))
        return swarm

    def move_swarm(self):
        for iter in range(self.iteration):
            # print iter
 
            for i in range(self.n_point):
                # reset neighbors_list
                self.swarm[i].neighbors_list[:] = [] 
                # Calculate objective function for each search agent
                self.swarm[i].current.fitness = self.func(self.swarm[i].current.position)
                # update each best
                if self.swarm[i].current.fitness < self.swarm[i].previous_best.fitness:
                    self.swarm[i].previous_best = deepcopy(self.swarm[i].current)
                # upfate globla k_best ,k_worst
                if self.swarm[i].current.fitness < self.globe_best.fitness:
                    self.globe_best = deepcopy(self.swarm[i].current)

                if self.swarm[i].current.fitness > self.globe_worst:
                    self.globe_worst = deepcopy(self.swarm[i].current)

            self.swarm = sorted(self.swarm, key= operator.attrgetter('current.fitness'))
  
            # (12)
            x_food_position = self.get_x_food_poition()
            x_food_fitness = self.func(x_food_position)
         
            #  Alpha, Beta, and Delta
            for i in range(self.n_point):
                # 2.2.1. Motion induced by other krill individuals
                sensing_distance = self.get_sensing_distance(i)
                for j in range(self.n_point):
                    if j is not i:
                        if np.linalg.norm(self.swarm[i].current.position - self.swarm[j].current.position ) < sensing_distance:
                            self.swarm[i].neighbors_list.append(j)
                # (3)
                Alpha = self.get_Alpha_local(i) + self.get_Alpha_target(i , iter)
                # (2)
                self.swarm[i].N = self.Nmax * Alpha + self.Wn * self.swarm[i].N
                # 2.2.2. Foraging motion
                # (11)
                Beta = self.get_Beta_food(i,iter ,x_food_position , x_food_fitness) + self.get_Beta_best(i)
                # (10)
                self.swarm[i].F = self.Vf * Beta + self.Wf * self.swarm[i].F

                # 2.2.3. Physical diffusion
                # (17)
                self.swarm[i].D = np.random.uniform(0.002, 0.010) * ( 1 - (iter / self.iteration)) * np.random.uniform(-1, 1)
                # (1)
                self.swarm[i].dX =  self.swarm[i].N + self.swarm[i].F + self.swarm[i].D

                # 2.2.4. Motion Process of the KH Algorithm

                self.swarm[i].current.position +=  self.delta_t * self.swarm[i].dX

                # check upper and lower bound
                for i in range(self.n_point):
                    for j in range(self.dimension):
                        if self.swarm[i].current.position[j] > self.max_bound:
                            self.swarm[i].current.position[j] = np.random.uniform(self.min_bound , self.max_bound)
                        if self.swarm[i].current.position[j] < self.min_bound:
                            self.swarm[i].current.position[j] = np.random.uniform(self.min_bound , self.max_bound)

            print iter , self.globe_best.fitness
        print np.array(self.globe_best.position)
        print self.globe_best.fitness


    def get_delta_t(self):
        sum = 0
        # here i think number of variables is dimension of each krill , and maybe each dimension has different range
        # but i set all dimension in the same range between min_bound and max_bound
        for i in range(self.dimension):
            sum += self.min_bound - self.max_bound
        return self.Ct * sum

    # (12)
    def get_x_food_poition(self):
        sum1 = 0
        sum2 = 0 
        for i in range(self.n_point):
            sum1 += (self.swarm[i].current.position / self.swarm[i].current.fitness)
            sum2 += (1 / self.swarm[i].current.fitness)
        return sum1 / sum2

    # (13)
    def get_Beta_food(self , i ,iter , x_food_position ,x_food_fitness):
        # (14)
        c_food = 2 * (1 - (iter / self.iteration))
        part1 = (self.swarm[i].current.fitness - x_food_fitness) / (self.globe_worst.fitness - self.globe_best.fitness)
        part2 = (x_food_position  - self.swarm[i].current.position ) / (np.linalg.norm(x_food_position  - self.swarm[i].current.position ) + self.tao)
        return c_food * part1 *part2

    # (15)
    def get_Beta_best(self,i):
        part1 = (self.swarm[i].current.fitness - self.swarm[i].previous_best.fitness) / (self.globe_worst.fitness - self.globe_best.fitness)
        part2 = (self.swarm[i].previous_best.position  - self.swarm[i].current.position ) / (np.linalg.norm(self.swarm[i].previous_best.position  - self.swarm[i].current.position ) + self.tao)
        
        return part1 * part2

    # (7)
    def get_sensing_distance(self,i):
        sum = 0
        for j in range(self.n_point):
            sum += np.linalg.norm(self.swarm[i].current.position  - self.swarm[j].current.position )
        #sum = sum / (5 * self.n_point)
        sum = sum / self.n_point
        return sum
    # (4)
    def get_Alpha_local(self,i):
        sum = 0
        for j in self.swarm[i].neighbors_list:    
            # (6)
            part1 = (self.swarm[i].current.fitness - self.swarm[j].current.fitness) / (self.globe_worst.fitness - self.globe_best.fitness)
            # (5)
            part2 = (self.swarm[j].current.position  - self.swarm[i].current.position ) / (np.linalg.norm(self.swarm[j].current.position  - self.swarm[i].current.position ) + self.tao)
            sum += (part1 * part2)
        return sum
    
    def get_Alpha_target(self,i,iter):
        # (9)
        c_best = 2 * (random.random() + (iter / self.iteration))
        # (8)
        part1 = (self.swarm[i].current.fitness - self.globe_best.fitness) / (self.globe_worst.fitness - self.globe_best.fitness)
        part2 = (self.globe_best.position  - self.swarm[i].current.position ) / (np.linalg.norm(self.globe_best.position  - self.swarm[i].current.position ) + self.tao)
        target = c_best * part1 * part2
        return target
