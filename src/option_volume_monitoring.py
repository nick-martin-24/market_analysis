#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:56:58 2019

@author: nickmartin
"""
import robin_stocks as r
import mail
import time
import datetime
import os
import market_utils
import numpy as np
import pandas as pd
import multiprocessing as mp
from tqdm import tqdm
from joblib import Parallel, delayed

def find_options(s,filename,columns):
    user = os.environ['robin_user']
    pwd = os.environ['robin_pass']
    r.login(user,pwd)
    options = {}

    all_options = r.options.find_tradable_options(s, optionType='call')
    options['call'] = pd.DataFrame(market_utils.get_options(all_options, datetime.date(2021,3,31), r.get_latest_price(s,includeExtendedHours=False)[0]))
    try:
        options['call']['ratio'] = options['call'].volume / options['call'].open_interest
        options['call'] = options['call'][(options['call'].ratio > 5) & (options['call'].ratio != np.inf) & (options['call'].volume >= 1000)].dropna()    
    except AttributeError as message:
        print('{} for {}'.format(message,s))

    if len(options['call']) > 0:
        options['put'] = pd.Series([r.options.find_options_by_expiration_and_strike(s,exp_date,strike,optionType='put')[0] for (exp_date,strike) in zip(options['call'].expiration_date,options['call'].strike_price)])
        options['call']['symbol'] = s
        options['call'].strike_price = options['call'].strike_price.astype(float)
        options['call'].last_trade_price = options['call'].last_trade_price.astype(float)
        options['call'].adjusted_mark_price = options['call'].adjusted_mark_price.astype(float)
        options['call'].previous_close_price = options['call'].previous_close_price.astype(float)
        options['call'].implied_volatility = options['call'].implied_volatility.astype(float)
        options['call'].chance_of_profit_long = options['call'].chance_of_profit_long.astype(float)
        options['call'].chance_of_profit_short = options['call'].chance_of_profit_short.astype(float)
        options['call']['put_volume'] = [x['volume'] for x in options['put']]
        options['call']['put_open'] = [x['open_interest'] for x in options['put']]
        options['call']['put_ratio'] = options['call']['put_volume'] / options['call']['put_open']

        options['call'].to_csv(filename,mode='a',header=False,columns=columns,index=False,float_format='%.2f')


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

    #symbols = symbols[100:200]
    #symbols = ['AAPL','TSLA','PLTR','ROKU']
    columns = ['symbol','expiration_date','strike_price','last_trade_price','money','volume','open_interest','ratio','put_volume','put_open','put_ratio','adjusted_mark_price','previous_close_price','implied_volatility','chance_of_profit_long','chance_of_profit_short']
    num_cores = mp.cpu_count()
    date_f = datetime.date.today().strftime('%Y%m%d')
    time_f = datetime.datetime.today().strftime('%H%M%S')
    outdir = '/Users/nickmartin/data/finance/{}/'.format(date_f)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    filename = '{}/unusual_{}_{}_{}_{}.csv'.format(outdir,'call','test',date_f,time_f)
    with open(filename,'w') as f:
        f.write('Symbol,Exp Date,Strike,Last Traded,Money,Volume,Open,Ratio,Put Vol.,Put Open,Put Ratio,Current Price,Prev Close Price,Imp Volatility,Long,Short\n')

    Parallel(n_jobs=num_cores)(delayed(find_options)(symbol,filename,columns) for symbol in tqdm(symbols))

    # read in .csv and sort by descending Ratio, with OTM at the top
    data = pd.read_csv(filename)
    data.Money = pd.Categorical(data['Money'],ordered=True)
    data = data.sort_values(['Money','Ratio'],ascending=False)
    data.to_csv(filename,index=False)

    # send file in email
    market_utils.mail_files(filename)
    print('Run time: {} seconds'.format(time.time() - start_time))

