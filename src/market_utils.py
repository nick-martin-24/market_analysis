import robin_stocks as r
import datetime
import calendar
import yagmail
import os
import matplotlib.pyplot as plt

def get_options(all_options,max_date,latest_price):
    options = []
    for option in all_options:
        y,m,d = option['expiration_date'].split('-')
        try:
            if datetime.date(int(y),int(m),int(d)) <= max_date:
                temp = r.get_option_market_data_by_id(option['id'])[0]
                temp['expiration_date'] = option['expiration_date']
                temp['strike_price'] = option['strike_price']
                temp['last_trade_price'] = latest_price
                if float(temp['last_trade_price']) - float(temp['strike_price']) > 0:
                    temp['money'] = 'ITM'
                else:
                    temp['money'] = 'OTM'
                options.append(temp)
        except TypeError as message:
            print('for options in all options {}: o man'.format(message))
        except IndexError as message:
            print('{} for {} {} {}'.format(message, r.get_symbol_by_url(option['url']), option['expiration_date'], option['type']))

    return options


def mail_files(files):
    sender = os.environ['gmail_addr']
    recipient = os.environ['gmail_addr']
    subject = '[UOA] {}'.format(datetime.date.today().strftime('%Y-%m-%d'))
    month = datetime.date.today().month
    day = datetime.date.today().day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = ['st','nd','rd'][day % 10 - 1]
    year = datetime.date.today().year
    body = 'Attached is the unusual options activity detected for {} {}{}, {}'.format(calendar.month_name[month], day, suffix, year)
    yag = yagmail.SMTP(sender)
    yag.send(
        to=recipient,
        subject=subject,
        contents=body, 
        attachments=files)


def plot_uoa_performance(s, exp, strike):
    data = r.get_option_historicals(s, exp, strike, 'call')
    dates = []
    prices = []
    for point in data:
        dates.append(datetime.datetime.strptime(point['begins_at'],'%Y-%m-%dT%H:%M:%SZ'))
        prices.append(float(point['open_price']))

    plt.plot(dates,prices)
    plt.show()
    
