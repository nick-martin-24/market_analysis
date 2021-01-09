from multiprocessing import Pool
import multiprocessing as mp
import robin_stocks as r
import option_utils
import os
from joblib import Parallel, delayed

def add(a,b):
    return a+b

def add5(a):
    return a+5

def test(s):
    user = os.environ['robin_user']
    pwd = os.environ['robin_pass']
    r.login(user,pwd)

    return r.options.find_tradable_options(s,optionType='call')

if __name__ == "__main__":
    pool = Pool()
    A=1
    B=3
    result1 = pool.apply_async(add,[A,B])
    result2 = pool.apply_async(add,[A,B])
    answer1 = result1.get(timeout=10)
    answer2 = result2.get(timeout=10)
    print(answer1)
    print(answer2)


    user = os.environ['robin_user']
    pwd = os.environ['robin_pass']
    r.login(user,pwd)

    a = 'AAPL'
    b = 'TSLA'
    c = 'AMZN'
    d = 'MSFT'
    #all_opts_a = r.options.find_tradable_options(a,optionType='call')
    #all_opts_b = r.options.find_tradable_options(b,optionType='call')
    #all_opts_c = r.options.find_tradable_options(c,optionType='call')
    #all_opts_d = r.options.find_tradable_options(d,optionType='call')
    #a_opts = pool.apply_async(test,[a])
    #b_opts = pool.apply_async(test,[b])
    #c_opts = pool.apply_async(test,[c])
    #d_opts = pool.apply_async(test,[d])
    #a_opts_ans = a_opts.get(timeout=10)
    #b_opts_ans = b_opts.get(timeout=10)
    #c_opts_ans = c_opts.get(timeout=10)
    #d_opts_ans = d_opts.get(timeout=10)
    num_cores = mp.cpu_count()
    inputs = [0,1,2,3,4,5,6,7,8,9]
    processed_list = Parallel(n_jobs=num_cores)(delayed(test(i)) for i in [a,b,c,d])
    #print(a_opts)
    #print(b_opts)
