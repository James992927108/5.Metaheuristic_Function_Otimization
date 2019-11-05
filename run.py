import math
import os
import sys
import time
from datetime import datetime as dt
from operator import attrgetter

import numpy as np

from benchmarks.cec05.cec05 import cec05
from benchmarks.cec17.cec17 import cec17
from benchmarks.paperfunction import paperfunction
from ffa import ffa
from goa.goa import goa
from gwo.gwo import gwo
from gwo.gwo_mgoaha import gwo_mgoaha
from kh import kh
from mbo import mbo
from ncs.ncs import ncs
from pso.pso import pso
from pso.spso2011 import spso2011
from result import result as rt
from woa import woa

sys.dont_write_bytecode = True


def write_file(file_name,value):
    fp = open(file_name, "a")
    fp.write(np.array2string(value))
    fp.close()

def creat_result_folder(directory):
    print directory
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def algo_map(algo_name):
    return {
        'pso': pso,
        'spso2011': spso2011,
        'gwo': gwo,
        'goa': goa,
        'gwo_mgoaha': gwo_mgoaha,
        # 'gwogoaha': gwogoaha,
    }.get(algo_name, 'gwo_mgoaha')


if __name__ == "__main__":

    roundtime = int(sys.argv[1])
    iteration = int(sys.argv[2])
    n_point = int(sys.argv[3])
    dimension = int(sys.argv[4])
    func_num = int(sys.argv[5])

    # func = F1_05
    cec = cec05(func_num, dimension)
    func = cec.func
    min_bound , max_bound = cec.getFunctionDetails(func_num)
    
    # p_cec = paperfunction(func_num, dimension)
    # func = p_cec.func
    # min_bound , max_bound = p_cec.getFunctionDetails(func_num)
    
    """
    algo :
        pso , spso2011 
        goa , 
        gwo , 
        woa , mbo , kh , ncs , ffa
    """

    select_algo = algo_map(str(sys.argv[6]))

    foldername = "{}-{}-{}-{}-{}-{}".format(select_algo.__name__,func_num,roundtime,iteration,n_point,dt.now().strftime('%Y%m%d'))
    directory_path = "result/{}/{}".format(func_num,foldername)
    creat_result_folder(directory_path)

    Round_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_Round")

    Position_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_Position")
    AveConvergence_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_AveConvergence")

    result_list = []
    for round in range(roundtime):

        start = time.time()

        algo = select_algo(func, min_bound, max_bound, dimension , n_point, iteration)            
        convergence_list , Agent = algo.move_swarm()
        
        result = rt(convergence_list , Agent.position)
        
        result_list.append(result)
        
        end = time.time()
        time_taken = end - start

        fp = open(Round_txt , "a")
        fp.write("Round: {} , Fun: {} , cost time : {} \n convergence_list : \n{} \n fitness : {}\n".format(round , func.__name__, time_taken , np.array2string(result._get_convergence_list()),result._get_min_convergence_list()))
        fp.close()

    round_max = max(result_list,key = attrgetter('min_fitness')).min_fitness
    round_ave = sum([result_list[i].min_fitness for i in range(len(result_list))]) / len(result_list)
    round_min = min(result_list,key = attrgetter('min_fitness')).min_fitness
    round_std = np.std([result_list[i].min_fitness for i in range(len(result_list))])
    fp = open(Round_txt, "a")
    fp.write("round \n max : {} \n ave : {} \n min : {} \n std : {} \n".format(round_max, round_ave, round_min, round_std ))
    fp.close()

    round_ave_convergence = sum([result_list[i].convergence_list for i in range(len(result_list))]) / len(result_list)
    round_min_position = min(result_list,key = attrgetter('min_fitness')).position

    write_file(AveConvergence_txt,round_ave_convergence)
    write_file(Position_txt,round_min_position)
