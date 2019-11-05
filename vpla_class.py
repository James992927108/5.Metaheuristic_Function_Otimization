import numpy as np

class Team:
    def __init__(self, fitness, formation ,substitute):
        self.fitness = fitness
        # self.position = position
        self.formation = formation
        self.substitute = substitute
        self.coach = 0

class vpla():
    def __init__(self,func,min_bound,max_bound,dimension,n_point,iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.delta_ks = 0
        self.N_ks = self.delta_ks * self.dimension

        self.swarms = self.init_swarm()

        # Identify Best team
        self.best_team = 0
        self.match_schedule = self.get_match_schedule()
        for i in self.match_schedule:
            print i 


    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            fitness = np.finfo(np.float32).max
            formation = np.random.uniform(0, 1,self.dimension) * (self.max_bound - self.min_bound) + self.min_bound
            substitute = np.random.uniform(0, 1,self.dimension) * (self.max_bound - self.min_bound) + self.min_bound
            swarm.append(Team(fitness, formation , substitute))
        return swarm
    
    def get_match_schedule(self):
        # idea : first get pair index 
        group_num = self.n_point / 2

        pair_index_list = self.get_pair_index_list(group_num)

        # second creat member_liat , it is single round robin when roundtime increase it will rotated clockwise
        single_round_robin_list = self.get_single_round_robin_list()
        match_schedule_list = []
        for i in range(len(single_round_robin_list)):
            temp_list = []
            for j in range(group_num):
                temp = [single_round_robin_list[i][pair_index_list[j][0]] ,  single_round_robin_list[i][pair_index_list[j][1]]]
                temp_list.append(temp)
            match_schedule_list.append(temp_list)

        return match_schedule_list

    def get_pair_index_list(self,group_num):
        pair_index_list = []
        for i in range(group_num):
            member1 = (self.n_point / 2) - i
            member2 = (self.n_point / 2) + 1 + i
            if member2 == self.n_point:
                member2 = 0
            group = [ member1,member2 ]
            pair_index_list.append(group)
        # print np.array(pair_index_list)
        return pair_index_list
    
    def get_single_round_robin_list(self):
        roundtime = self.n_point
        single_round_robin_list = []
        for round in range(roundtime):
            if round is not 0:
                single_round_robin= [(round +i) % (self.n_point) for i in range(self.n_point)]
                if 0 in single_round_robin:
                    del single_round_robin[single_round_robin.index(0)]
                single_round_robin.insert(0 , 0)
                single_round_robin_list.append(single_round_robin)
        # print np.array(single_round_robin_list)
        return single_round_robin_list
if __name__ == "__main__":
    iteration = 1000

    n_point = 10
    dimension = 5

    min_bound = -500
    max_bound = 500

    func = 0

    a = vpla(func, min_bound, max_bound,dimension, n_point, iteration)