import multiprocessing as mp
import time
import math

results_a = []
results_b = []
results_c = []

def make_calculation_one(numbers):
    for number in numbers:
        results_a.append(math.sqrt(number**3))

def make_calculation_two(numbers):
    for number in numbers:
        results_b.append(math.sqrt(number**4))

def make_calculation_three(numbers):
    for number in numbers:
        results_b.append(math.sqrt(number**5))

if __name__ == "__main__":
    
    number_list = list(range(5000000))

    # Create the different procesese
    p1 = mp.Process(target=make_calculation_one,args=(number_list,))
    p2 = mp.Process(target=make_calculation_two,args=(number_list,))
    p3 = mp.Process(target=make_calculation_three,args=(number_list,))

    start = time.time()
    p1.start()
    p2.start()
    p3.start()
    end = time.time()
    print("Time is :" , end-start)

#%%
import multiprocessing
import numpy as np
import time

def task(x):

    return x**(-0.5)

values = np.arange(1,10000000)

if __name__ == "__main__":

    # Loop
    start = time.time()
    res = []
    for i in values:
        res.append(task(i))
    stop = time.time()

    print("Elapsed time loop is :", stop-start)

    start = time.time()
    # create a process pool that uses all cpus
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # close the process pool
    x = pool.map(task, values)
    pool.close()
    stop = time.time()

    print("Elapsed time pararell is:", stop-start)
# %%
