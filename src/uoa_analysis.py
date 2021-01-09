import robin_stocks as r
import market_utils
import argparse

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-s',type=str,action='store',default='AAPL',help='symbol')

    p.add_argument('-d',type=str,action='store',default='2021-01-29',help='expiration date')

    p.add_argument('-p',type=str,action='store',default='150',help='strike price')
    args = p.parse_args()

    symbol = args.s
    exp_date = args.d
    strike = args.p

    print(vars(args))
    market_utils.login()
    market_utils.plot_uoa_performance(symbol,exp_date,strike)
