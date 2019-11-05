I have finish some metaheuristic algorithm , all are based on population(swarms - intelligent)
-> pso
-> spso2011
-> gwo(Grey Wolf Optimizer , 2014)
-> woa(The Whale Optimization Algorithm , 2016)
-> goa(Grasshopper Optimisation Algorithm: Theory and application , 2017)
-> mbo(Monarch Butterfly Optimization , 2015)
-> kh(Krill herd: A new bio-inspired optimization algorithm , 2012)
-> ncs(Negatively Correlated Search , 2016)
-> ffa(Firefly Algorithms , 2009)

what's package required?
numpy
how to run ?
$ python run.py

test function:
In version 0.7 ,add cec2017 benchmarks,
the code is modifty by c-version which provide by cec office

every algorithm class use the same parameter , and those parameter can set by ourself
in run.py , for example :

cec = cec17(func_num, dimension)
func = cec.func
min_bound = -500
max_bound = 500
dimension = 30
n_point = 40
iteration = 100

initial first , all the update mechanism is in move_swarm()
algo = spso2011(F1,min_bound,max_bound,dimension,n_point,iteration)
algo.move_swarm()

different algorithm have different parameter in the update , i set those parameter in algorithm
class , for example,
pso have w , c1 ,c2 . i set value in the pso

vesrion :
version 0.1 finish pso.py and spso2011.py
vesrion 0.2 finish gwo.py and woa.py
version 0.5 finish ncs.py (performance test on function F8 is weak.)
version 0.6 finish ffa.py
version 0.7 加入 cec2017 benchmarks
            cec17.py need to pass two parameter to cec17 class for init,
            first is func_num ,mean which function select , cec2017 have 28 functions, so 
            the input is between 1 to 28. dimension is according to dataset , in cec2017 have provide file
            cec2017 has specification the dimension, only 10 ,30 ,50 ,100 are available.
            for example :
            can import cec17 to you want file, 
            $ python run.py 
            from benchmarks.cec17 import cec17

            for func_num in range(1,28):
                cec = cec17(func_num, dimension)
                func = cec.func
        0.7.1 add result to output file
version 0.8 加入 cec2005 benchmarks
