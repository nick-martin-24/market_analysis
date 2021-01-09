#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:56:58 2019

@author: nickmartin
"""
import robin_stocks as r
import time
import datetime
import os
import option_utils
import multiprocessing as mp
from joblib import Parallel, delayed

def find_options(s):
    date_f = datetime.date.today().strftime('%Y%m%d')
    time_f = datetime.datetime.today().strftime('%H%M%S')    
    outdir = '/Users/nickmartin/data/finance/{}/'.format(date_f)    
    filename = '{}/unusual_{}_{}_{}_{}.csv'.format(outdir,'call','test',date_f,time_f)

    user = os.environ['robin_user']
    pwd = os.environ['robin_pass']
    r.login(user,pwd)

    all_options = r.options.find_tradable_options(s, optionType='call')
    options = option_utils.get_options(all_options, datetime.date(2020,3,31), r.get_latest_price(s,includeExtendedHours=False)[0])
    option_utils.write_uoa_file(filename,s,options)

if __name__ == '__main__':
    start_time = time.time()


    user = os.environ['robin_user']
    pwd = os.environ['robin_pass']
    r.login(user,pwd)
    api_market_header = 'https://api.robinhood.com/markets/'
    markets = ['{}XNYS/'.format(api_market_header),
           '{}XNAS/'.format(api_market_header),
           '{}XASE/'.format(api_market_header)]
    instrument_data = r.find_instrument_data('')
    remove_markets = [item for item in instrument_data if item['market'] in markets]
    remove_untradable = [item for item in remove_markets if item['rhs_tradability'] == 'tradable']
    remove_no_chain_id = [item for item in remove_untradable if item['tradable_chain_id'] is not None]
    symbols = [item['symbol'] for item in remove_no_chain_id]

    symbols = symbols[0:50]
    #symbols = ['AAPL','TSLA','MSFT','NKLA']
    type_errors = []
    option_types = ['call']
    num_cores = mp.cpu_count()
    pool = mp.Pool(num_cores)
    date_f = datetime.date.today().strftime('%Y%m%d')
    time_f = datetime.datetime.today().strftime('%H%M%S')
    outdir = '/Users/nickmartin/data/finance/{}/'.format(date_f)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    filename = '{}/unusual_{}_{}_{}_{}.csv'.format(outdir,'call','test2',date_f,time_f)
    
    with open(filename,'w') as f:
        f.write('Symbol,Exp Date,Strike,Last Traded,Money,Volume,Open,Ratio,Current Price,Prev Close Price,Imp Volatility,Long,Short\n')
    
    pool.map(find_options,symbols)
    print('Run time: {} seconds'.format(time.time() - start_time))





