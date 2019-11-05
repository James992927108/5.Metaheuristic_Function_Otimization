
class result():
    def __init__(self,convergence_list,position):
        self.convergence_list = convergence_list
        self.min_fitness = min(self.convergence_list)
        self.position = position

    def _get_convergence_list(self):
        return self.convergence_list
    
    def _get_min_convergence_list(self):
        return min(self.convergence_list)

    def _get_position(self):
        return self.position