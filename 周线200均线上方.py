#-*- codeing = utf-8 -*-


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
binan200Z = []

def crawl_exchanges_dates(exchange_name,symbol,start_time,end_time):
    try:
        exchange_class = getattr(ccxt,exchange_name) #获取交易所名称，ccxt.binance
        exchange = exchange_class()  #交易所的类，类似ssxt.bitfinex（）
        print(exchange)

        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        start_time_stamp = int(time.mktime(start_time.timetuple())) *1000
        end_time_stamp = int(time.mktime(end_time.timetuple())) *1000

        date = exchange.fetch_ohlcv(symbol, timeframe='1w', since=start_time_stamp, limit=500)
        if len(date) == 0:
            print(f"{symbol}数据为空")
            return
        df = pd.DataFrame(date)
        df.rename(columns={0:'open_time',1:'open',2:'high',3:'low',4:'close',5:'volume'},inplace=True)
        # df.set_index('open_time', drop=True, inplace=True)

        # exit()
        df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60)



        df['Datetime'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
        df['Datetime'] = df['Datetime'].apply(lambda x: str(x)[0:19])
        df.drop_duplicates(subset=['open_time'], inplace=True)
        df.set_index('Datetime', inplace=True)
        print("*" * 20)
        df['ma200'] = ta.MA(df['close'], timeperiod=200)
        ma200 = df.iloc[-2]['ma200']
        ma = df.iloc[-2]['close']
        ma20020 = ma200 * 0.05 + ma200
        print(ma200)
        print(ma)

        if ma > ma200:

            binan200Z.append(symbol)
            print(f'{symbol}符合')
        else:

            print(f'{symbol}不符合')

            print(binan200Z)
            print(f'币安周线200以上一共{len(binan200Z)}个')
            print("*" * 40)
    except:
        print(f"{symbol}数据请求错误，跳过")
        return


if __name__=='__main__':
    now = int(time.time())
    last = int(now - 2150000 * 60)
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
            # sample_dates('binance', usdt)
            # clear_dates('binance', usdt)
        except KeyError:
            pass
        continue

    caiji_time = time.strftime("%Y-%m-%d日%H", end)
    filename = str(caiji_time) + '点的周线200以上' + '.txt'
    with open(filename, 'w') as f:
        f.write(str(binan200Z))
    print(f'{str(caiji_time)}点采集完毕')




