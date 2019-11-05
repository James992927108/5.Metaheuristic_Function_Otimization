import math
import random
import numpy as np
import operator
from copy import deepcopy

class Agent:
    def __init__(self, position , fitness, sigma):
        self.position = position

        self.fitness = fitness

        self.pCorr = 0
        self.trialCorr = 0

        self.sigma = sigma


class ncs:
    def __init__(self,func,min_bound,max_bound,dimension,n_point,iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.swarms = self.init_swarm()
        self.u_swarms = deepcopy(self.swarms)

    def init_swarm(self):
        swarms = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound,self.dimension)
            fitness = self.func(position)
            sigma = np.random.uniform(self.min_bound , self.max_bound ,self.dimension) / self.n_point
            swarms.append(Agent( position , fitness , sigma))
        return swarms  


    def move_swarm(self):
        self.swarms = sorted(self.swarms, key= operator.attrgetter('fitness'))
        bestfound = deepcopy(self.swarms[0])
        
        r = 0.99
        lambda_t = np.ones(self.n_point)
        lambda_sigma = 0.1
        lambda_range = lambda_sigma
        flag = np.zeros(self.n_point)

        for iter in range(self.iteration):
            for i in range(self.n_point):
                # (5)
                self.u_swarms[i].position = deepcopy(self.swarms[i].position + self.swarms[i].sigma * np.random.uniform(self.dimension,self.n_point))
                for j in range(self.dimension):
                    if self.u_swarms[i].position[j] > self.max_bound:
                        self.u_swarms[i].position[j] = self.max_bound
                    elif self.u_swarms[i].position[j] < self.min_bound:
                        self.u_swarms[i].position[j] = self.min_bound
                # pseudo-code line 9                
                self.u_swarms[i].fitness = self.func(self.u_swarms[i].position)
                # pseudo-code line 12
                if self.u_swarms[i].fitness < bestfound.fitness:
                    bestfound = deepcopy(self.u_swarms[i])
            
            normTrialFit = np.zeros(self.n_point)
            for i in range(self.n_point):
                tempFit = self.swarms[i].fitness - bestfound.fitness
                tempTrialFit = self.u_swarms[i].fitness - bestfound.fitness
                normTrialFit[i] = tempTrialFit / (tempFit + tempTrialFit)
            
            pMinCorr , trialMinCorr = self.get_min_p_and_trial()
            normTrialCorr = trialMinCorr / (pMinCorr + trialMinCorr)
            # pseudo-code line 6
            lambda_t = 1 + lambda_sigma * np.random.uniform(0,1,self.n_point)
            lambda_sigma = lambda_range - lambda_range * iter / self.iteration
            for i in range(self.n_point):
                # pseudo-code line 15
                if lambda_t[i] * normTrialCorr[i] > normTrialFit[i]:
                    self.swarms[i] = deepcopy(self.u_swarms[i])
                    flag[i] += 1

            if iter % self.n_point == 0:
                for i in range(self.n_point):
                    if flag[i] / self.n_point > 0.2:
                        self.swarms[i].sigma = self.swarms[i].sigma / r
                    elif(flag[i] / self.n_point) < 0.2:
                        self.swarms[i].sigma = self.swarms[i].sigma * r
                flag = np.zeros(self.n_point)
            print iter , bestfound.fitness
        print np.array(bestfound.position)
        return bestfound

    # calculate the Bhattacharyya distance
    # (7)
    def get_min_p_and_trial(self):
        pCorr = np.ones((self.n_point , self.n_point)) * np.finfo(np.float32).max
        trialCorr = np.ones((self.n_point , self.n_point)) * np.finfo(np.float32).max
        for i in range(self.n_point):
            for j in range(self.n_point):
                if j is not i:
                    part1 = np.matrix(self.swarms[i].position - self.swarms[j].position)
                    part2 = (self.swarms[i].sigma**2 + self.swarms[j].sigma**2)/2
                    part3 = 0
                    for k in range(self.dimension):
                        # in here i add abs in the formule before do the sqrt
                        part3 += math.log(part2[k]) / (math.sqrt(abs(math.log(self.swarms[i].sigma[k]**2) * math.log(self.swarms[j].sigma[k]**2))))
                    # part3 = 0
                    # for k in range(self.dimension):
                    #     part3 += math.log(part2[k]) - 0.5 * (math.sqrt(math.log(self.swarms[i].sigma[k]**2) + math.log(self.swarms[j].sigma[k]**2)))
                    pCorr[i , j] = ((part1 * np.diag(1 / part2) * part1.T) / 8) + ( 1 / 2) * math.log(part3)

                    part1 = np.matrix(self.u_swarms[i].position - self.u_swarms[j].position)
                    trialCorr[i,j] = ((part1 * np.diag(1 / part2) * part1.T) / 8) + ( 1 / 2) * math.log(part3)
        # return each row samll vale , so pCorr.min(1) is a vector
        return pCorr.min(1) , trialCorr.min(1)