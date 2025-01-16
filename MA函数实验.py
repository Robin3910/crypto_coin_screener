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
binan4Hk = []
binan4Hv = []

pd.set_option('expand_frame_repr', False)

def crawl_exchanges_dates(exchange_name,symbol,timeframe,aver,manymin):
    exchange_class = getattr(ccxt,exchange_name) #获取交易所名称，ccxt.binance
    exchange = exchange_class()  #交易所的类，类似ssxt.bitfinex（）
    print(exchange)

    last = time.time() - (aver + 5) * 60 * manymin
    start = time.localtime(last)
    start_time = time.strftime("%Y-%m-%d", start)
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    start_time_stamp = int(time.mktime(start_time.timetuple())) *1000
    print(start_time)

    date = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=start_time_stamp, limit=1000)
    if len(date) == 0:
        print(f"{symbol}数据为空")
        return None, None, None, None, None, None, None, None, None, None, None, None
    df = pd.DataFrame(date)
    df.rename(columns={0:'open_time',1:'open',2:'high',3:'low',4:'close',5:'volume'},inplace=True)

    df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60)
    df['Datetime'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    df['Datetime'] = df['Datetime'].apply(lambda x: str(x)[0:19])
    df.drop_duplicates(subset=['open_time'], inplace=True)
    df.set_index('Datetime', inplace=True)
    print("*" * 20)

    df[f'ma{aver}'] = ta.MA(df['close'], timeperiod=aver)

    print(df)

    try:
        x1 = df.iloc[-2][f'ma{aver}']
        ma = df.iloc[-2]['close']
        return x1,ma
        # exit()
        # ma2020 = ma20 - ma20 * 0.1
        # ma = df.iloc[-2]['close']
        #
        # if  ma20 > ma > ma2020:
        #
        #     binan4Hk.append(symbol)
        #     binan4Hv.append(ma)
        #     print(f'{symbol}符合')
        # else:
        #
        #     print(f'{symbol}不符合')
        #
        #     print(binan4Hk)
        #     print(f'币安日线20均线下方百分之10以内一共{len(binan4Hk)}个')
        #     print("*" * 40)
    except IndexError:
        pass


if __name__=='__main__':


    binance = ccxt.binance()
    binance.load_markets()
    symbols = binance.symbols
    usdts = []
    for symbol in symbols:
        if symbol[-4:] == 'USDT':
            usdts.append(symbol)
    print(usdts)

    for usdt in usdts:
        try:
            ma200,ma = crawl_exchanges_dates('binance', usdt,'1d',200,1440)
            if ma200 is None:
                continue

            ma2020 = float(ma200) - float(ma200) * 0.1


            if  ma200 > ma > ma2020:

                binan4Hk.append(usdt)
                binan4Hv.append(ma)
                print(f'{usdt}符合')
            else:

                print(f'{usdt}不符合')

                print(binan4Hk)
                print(f'币安日线20均线下方百分之10以内一共{len(binan4Hk)}个')
                print("*" * 40)

        except (KeyError,TypeError):
            pass
        continue


    current_path = os.getcwd()
    file_dir = os.path.join(current_path,'币安日线20均线下方百分之10以内')

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    now = int(time.time())
    # last = int(now - 403200 * 60)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    end = time.localtime(now)
    caiji_time = time.strftime("%Y-%m-%d日%H", end)
    filename = str(caiji_time) + '点ma在日线20均线下方百分之10以内所有币' + '.txt'
    with open(f'{file_dir}//{filename}', 'w') as f:
        f.write(str(binan4Hk))

    filename1 = str(caiji_time) + '点ma日线20均线下方百分之10以内价格' + '.txt'
    with open(f'{file_dir}//{filename1}', 'w') as f1:
        f1.write(str(binan4Hv))
    print(f'{str(caiji_time)}点采集完毕')


