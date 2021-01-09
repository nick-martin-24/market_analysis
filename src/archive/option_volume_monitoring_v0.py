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

symbols = symbols[0:500]
#symbols = ['AAPL','TSLA','PLTR','ROKU']
#symbols = ['TSLA']
max_date = datetime.date(2021,3,31)
limit = 0.2
type_errors = []
option_types = ['call']
if len(symbols) == 1:
    suffix = symbols[0]
else:
    suffix = '{}symbols'.format(len(symbols))

date_f = datetime.date.today().strftime('%Y%m%d')
time_f = datetime.datetime.today().strftime('%H%M%S')
outdir = '/Users/nickmartin/data/finance/{}/'.format(date_f)
if not os.path.exists(outdir):
    os.makedirs(outdir)
for option_type in option_types:
    filename = '{}/unusual_{}_{}_{}_{}.csv'.format(outdir,option_type,suffix,date_f,time_f)
    with open(filename,'w') as f:
        f.write('Symbol,Exp Date,Strike,Last Traded,Money,Volume,Open,Ratio,Current Price,Prev Close Price,Imp Volatility,Long,Short\n')

    count = 1
    for symbol in symbols:
        print('processing {} {} of {}: {}'.format(option_type,count,len(symbols),symbol))
        count += 1
        try:
            all_options = r.options.find_tradable_options(symbol,optionType=option_type)
        except TypeError as message:
            print('for symbol in symbols {}: o man'.format(message))

        options,good_options,bad_options = option_utils.get_options(all_options,max_date,r.get_latest_price(symbol,includeExtendedHours=False)[0])
        option_utils.write_uoa_file(filename, symbol, options)

print('Run time: {} seconds'.format(time.time() - start_time))


