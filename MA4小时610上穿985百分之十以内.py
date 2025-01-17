#-*- codeing = utf-8 -*-
#@Time : 2021/11/18 17:59
#@Author : 赵旭辉
#@File : MA4小时多均线接近.py
#@Software ： PyCharm
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

def crawl_exchanges_dates(exchange_name,symbol,timeframe,aver1,aver2,aver3,aver4,aver5,aver6,aver7,aver8,manymin):
    try:
        
        exchange_class = getattr(ccxt,exchange_name) #获取交易所名称，ccxt.binance
        exchange = exchange_class()  #交易所的类，类似ssxt.bitfinex（）
        print(exchange)

        last = time.time() - (aver8 + 5) * 60 * manymin
        start = time.localtime(last)
        start_time = time.strftime("%Y-%m-%d %H-%M-%S", start)
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H-%M-%S')
        start_time_stamp = int(time.mktime(start_time.timetuple())) *1000
        print(start_time)

        date = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=start_time_stamp, limit=1000)
        if len(date) == 0:
            print(f"{symbol}数据为空")
            return 
        df = pd.DataFrame(date)
        df.rename(columns={0:'open_time',1:'open',2:'high',3:'low',4:'close',5:'volume'},inplace=True)

        df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60)
        df['Datetime'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)
        df['Datetime'] = df['Datetime'].apply(lambda x: str(x)[0:19])
        df.drop_duplicates(subset=['open_time'], inplace=True)
        df.set_index('Datetime', inplace=True)
        print("*" * 20)

        df[f'ma{aver1}'] = ta.MA(df['close'], timeperiod=aver1)
        df[f'ma{aver2}'] = ta.MA(df['close'], timeperiod=aver2)
        df[f'ma{aver3}'] = ta.MA(df['close'], timeperiod=aver3)
        df[f'ma{aver4}'] = ta.MA(df['close'], timeperiod=aver4)
        df[f'ma{aver5}'] = ta.MA(df['close'], timeperiod=aver5)
        df[f'ma{aver6}'] = ta.MA(df['close'], timeperiod=aver6)
        df[f'ma{aver7}'] = ta.MA(df['close'], timeperiod=aver7)
        df[f'ma{aver8}'] = ta.MA(df['close'], timeperiod=aver8)


        x1 = df.iloc[-2][f'ma{aver1}']
        x2 = df.iloc[-2][f'ma{aver2}']
        x3 = df.iloc[-2][f'ma{aver3}']
        x4 = df.iloc[-2][f'ma{aver4}']
        x5 = df.iloc[-2][f'ma{aver5}']
        x6 = df.iloc[-2][f'ma{aver6}']
        x7 = df.iloc[-2][f'ma{aver7}']
        x8 = df.iloc[-2][f'ma{aver8}']
        maclose = df.iloc[-2]['close']
        maopen = df.iloc[-2]['open']
        return x1,x2,x3,x4,x5,x6,x7,x8,maclose,maopen
    except:
        print(f'{symbol}获取数据错误')
        return


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
            # zma5, zma10, zma20, zma24, zma25, zma26, zma27, zma28, zma = crawl_exchanges_dates('binance', usdt, '1w', 5, 10, 20, 24, 25, 26, 27, 28, 10080)
            # zma2020 = float(zma20) + float(zma20) * 0.2
            #
            # rma5, rma10, rma20, rma30, rma35, rma36, rma37, rma38, rma = crawl_exchanges_dates('binance', usdt, '1d', 5 ,10 , 20, 30, 35, 36, 37, 38, 1440)
            # rma3020 = float(rma30) + float(rma30) * 0.2

            mma5, mma10, mma20, mma30, mma60, mma90, mma610, mma985, mmaclose,mmaopen = crawl_exchanges_dates('binance', usdt, '4h', 5, 10, 20, 30, 60, 90, 610, 985, 240)
            
                        
            if mma5 is None:
                continue
            mma98510 = float(mma985) + float(mma985) * 0.1




            if mma98510 > mma610 > mma985:

                binan4Hk.append(usdt)
                binan4Hv.append(mmaclose)
                print(f'{usdt}符合')
            else:

                print(f'{usdt}不符合')

                print(binan4Hk)
                print(f'币安4小时610上穿985百分之十以内一共{len(binan4Hk)}个')
                print("*" * 40)

        except (KeyError,TypeError):
            pass
        continue


    current_path = os.getcwd()
    file_dir = os.path.join(current_path,'币安4小时610上穿985百分之十以内测试')

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    now = int(time.time())
    # last = int(now - 403200 * 60)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    end = time.localtime(now)
    caiji_time = time.strftime("%Y-%m-%d日%H", end)
    filename = str(caiji_time) + '点ma4小时610上穿985百分之十以内测试所有币' + '.txt'
    with open(f'{file_dir}//{filename}', 'w') as f:
        f.write(str(binan4Hk))

    filename1 = str(caiji_time) + '点ma4小时610上穿985百分之十以内当前收盘价格' + '.txt'
    with open(f'{file_dir}//{filename1}', 'w') as f1:
        f1.write(str(binan4Hv))
    print(f'{str(caiji_time)}点采集完毕')


