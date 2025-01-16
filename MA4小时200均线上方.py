#-*- codeing = utf-8 -*-
#@Time : 2021/10/31 12:30
#@Author : 赵旭辉
#@File : 第二十二课ccxt爬取交易所数据.py
#@Software ： PyCharm

import pandas as pd
import time
import os
import datetime
import ccxt
import talib as ta




pd.set_option('expand_frame_repr', False)

TIMEOUT = 6 #6 second
BITFINEX_LIMIT = 5000
BITMEX_LIMIT = 500
BINANCE_LIMIT = 500
binan4Hk = []
binan4Hv = []


def crawl_exchanges_dates(exchange_name,symbol,start_time,end_time):

    exchange_class = getattr(ccxt,exchange_name) #获取交易所名称，ccxt.binance
    exchange = exchange_class()  #交易所的类，类似ssxt.bitfinex（）
    print(exchange)

    # current_path = os.getcwd()
    # file_dir = os.path.join(current_path,exchange_name+'5m',symbol.replace('/',''))
    #
    # if not os.path.exists(file_dir):
    #     os.makedirs(file_dir)

    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    start_time_stamp = int(time.mktime(start_time.timetuple())) *1000
    end_time_stamp = int(time.mktime(end_time.timetuple())) *1000



    date = exchange.fetch_ohlcv(symbol, timeframe='4h', since=start_time_stamp, limit=500)
    if len(date) == 0:
        print(f"{symbol}数据为空")
        return None, None, None, None, None, None, None, None, None, None, None, None
    df = pd.DataFrame(date)
    df.rename(columns={0:'open_time',1:'open',2:'high',3:'low',4:'close',5:'volume'},inplace=True)
    # df.set_index('open_time', drop=True, inplace=True)

    print(df)
    # exit()
    df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60)



    df['Datetime'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    df['Datetime'] = df['Datetime'].apply(lambda x: str(x)[0:19])
    df.drop_duplicates(subset=['open_time'], inplace=True)
    df.set_index('Datetime', inplace=True)
    print("*" * 20)
    df['ma250'] = ta.MA(df['close'], timeperiod=250)
    df['ma200'] = ta.MA(df['close'], timeperiod=200)
    df['ma169'] = ta.MA(df['close'], timeperiod=169)
    df['ma144'] = ta.MA(df['close'], timeperiod=144)
    df['ma20'] = ta.MA(df['close'], timeperiod=20)
    df['ma5'] = ta.MA(df['close'], timeperiod=5)
    print(df)

    try:
        ma250 = df.iloc[-2]['ma250']
        ma200 = df.iloc[-2]['ma200']
        ma169 = df.iloc[-2]['ma169']
        ma144 = df.iloc[-2]['ma144']
        ma16910 = ma169 + ma169 * 0.1
        ma20 = df.iloc[-2]['ma20']
        ma205 = ma20 + ma20 * 0.1
        ma5 = df.iloc[-2]['ma5']
        ma = df.iloc[-2]['close']


        print(ma)
        # print(ma16920)
        # print(ma14420)

        if ma > ma200:

            binan4Hk.append(symbol)
            binan4Hv.append(ma)
            print(f'{symbol}符合')
        else:

            print(f'{symbol}不符合')

            print(binan4Hk)
            print(f'币安4小时200均线上方一共{len(binan4Hk)}个')
            print("*" * 40)
    except IndexError:
        pass


if __name__=='__main__':
    now = int(time.time())
    last = int(now - 63200 * 60)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    end = time.localtime(now)
    start = time.localtime(last)
    end_time = time.strftime("%Y-%m-%d", end)
    start_time = time.strftime("%Y-%m-%d", start)
    print(end_time)
    print(start_time)

    binance = ccxt.binance()
    binance.load_markets()
    symbols = binance.symbols
    # print(symbols)
    usdts = []
    for symbol in symbols:
        if symbol[-4:] == 'USDT':
            usdts.append(symbol)
    print(usdts)

    for usdt in usdts:
        try:
            crawl_exchanges_dates('binance', usdt, start_time, end_time)

        except KeyError:
            pass
        continue

    current_path = os.getcwd()
    file_dir = os.path.join(current_path,'币安4小时200均线上方')

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    caiji_time = time.strftime("%Y-%m-%d日%H", end)
    filename = str(caiji_time) + '点ma在200以上所有币' + '.txt'
    with open(f'{file_dir}//{filename}', 'w') as f:
        f.write(str(binan4Hk))
    # print(f'{str(caiji_time)}点采集完毕')

    filename1 = str(caiji_time) + '点ma在200以上价格' + '.txt'
    with open(f'{file_dir}//{filename1}', 'w') as f1:
        f1.write(str(binan4Hv))
    print(f'{str(caiji_time)}点采集完毕')


