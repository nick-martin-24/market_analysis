#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 20:28:32 2019

@author: nickmartin
"""
import robin_stocks as r
import mail
import time
import datetime
import os
import market_utils as mutils
start_time = time.time()

mutils.login()
stop_loss_file = '/Users/nickmartin/personal/finance/stop_loss.txt'
gains_file = '/Users/nickmartin/personal/finance/gains.txt'

stop_loss = -50
gains = 50

# ============================================================
# Load in list of previously flagged stop loss events
# ============================================================    
flagged_stop_loss = []
with open(stop_loss_file,'r') as f:
    for line in f:
        flagged_stop_loss.append(line.strip())

flagged_gains = []
with open(gains_file,'r')as f:
    for line in f:
        flagged_gains.append(line.strip())
   

     
stop_loss_list = []
gains_list = []
open_options = r.options.get_open_option_positions()

# ============================================================
# Calculate percent change of each currently held option, and
# add it to stop_loss if it has declined 50% and has not been
# flagged before
# ============================================================    
for option in open_options:
    option_data = r.helper.request_get(option['option'],'regular')
    symbol = option['chain_symbol']
    string = '{} {} {} {}'.format(symbol,option_data['expiration_date'],float(option_data['strike_price']),option_data['type'])
    start_price = float(option['average_price'])/100
    
    current_option_state = r.options.find_options_for_stock_by_expiration_and_strike(symbol,option_data['expiration_date'],float(option_data['strike_price']),option_data['type'])[0]
    current_price = float(current_option_state['adjusted_mark_price'])
    percent_change = 100 * (current_price - start_price) / start_price
    if percent_change <= stop_loss:
        if string not in flagged_stop_loss:
            stop_loss_list.append(symbol)
            subject = '[STOP LOSS] {}'.format(string)
            body = '{} has moved {:.02f}%.'.format(symbol,percent_change)
            mail.send_mail(user,subject,body)
            with open(stop_loss_file, 'a') as f:
                f.write('{}\n'.format(string))
    
    if percent_change >= gains:
        if string not in flagged_gains:
            gains_list.append(symbol)
            subject = '[GAINS] {}'.format(string)
            body = '{} has moved {:.02f}%.'.format(symbol,percent_change)
            mail.send_mail(user,subject,body)
            with open(gains_file,'a') as f:
                f.write('{}: {}\n'.format(string))
#                f.write('{}: {}\n'.format(datetime.datetime.now().strftime('%m-%d-%Y %H:%M'),string))


print('Run time: {} seconds'.format(time.time() - start_time))

