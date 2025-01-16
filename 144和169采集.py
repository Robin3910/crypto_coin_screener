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
binan4H = []

def crawl_exchanges_dates(exchange_name,symbol,start_time,end_time):
    try:
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
        df['ma169'] = ta.MA(df['close'], timeperiod=169)
        df['ma144'] = ta.MA(df['close'], timeperiod=144)
        print(df)
        ma169 = df.iloc[-2]['ma169']
        ma144 = df.iloc[-2]['ma144']
        ma = df.iloc[-2]['close']
        ma16920 = ma169*0.05 + ma169
        ma14420 = ma144*0.05 + ma144
        print(ma169)
        print(ma144)
        print(ma)
        print(ma16920)
        print(ma14420)



        if ma > ma169 and ma > ma144 and ma < ma16920 and ma < ma14420:

            binan4H.append(symbol)
            print(f'{symbol}符合')
        else:

            print(f'{symbol}不符合')

            print(binan4H)
            print(f'币安4小时169和144一共{len(binan4H)}个')
            print("*" * 40)
    except:
        print(f"{symbol}数据请求错误，跳过")
        return None, None, None, None, None, None, None, None, None, None, None, None



    # limit_count = 500
    # if exchange_name == 'bitfinex':
    #     limit_count = BITFINEX_LIMIT
    # elif exchange_name == 'bitmex':
    #     limit_count = BITMEX_LIMIT
    # elif exchange_name == 'binance':
    #     limit_count == BINANCE_LIMIT

    # while True:
    #     try:
    #
    #         print(start_time_stamp)
    #         date = exchange.fetch_ohlcv(symbol,timeframe='4h',since=start_time_stamp,limit=500)
    #         df = pd.DataFrame(date)
    #         df.rename(columns={0:'open_time',1:'open',2:'high',3:'low',4:'close',5:'volume'},inplace=True)
    #
    #         start_time_stamp = int(df.iloc[-1]['open_time'])  #获取下一次请求的时间
    #
    #         filename = str(start_time_stamp) + '.csv'
    #         save_file_path = os.path.join(file_dir,filename)
    #
    #         print("文件保存路径为：%s" % save_file_path)
    #
    #         df.set_index('open_time',drop=True,inplace=True)
    #         df.to_csv(save_file_path)
    #
    #         if start_time_stamp > end_time_stamp:
    #             print("完成数据请求。")
    #             break
    #         time.sleep(2)
    #
    #     except Exception as error:
    #         print(error)
    #         time.sleep(10)


# def sample_dates(exchange_name,symbol):
#
#     path = os.path.join(os.getcwd(),exchange_name+'5m',symbol.replace('/',''))
#     # print(path)
#
#
#     file_path = []
#     for root,dirs,files in os.walk(path):
#         if files:
#             for file in files:
#                 if file.endswith('.csv'):
#                     file_path.append(os.path.join(path,file))
#
#     file_path = sorted(file_path)
#     all_df = pd.DataFrame()
#
#     for file in file_path:
#         df = pd.read_csv(file)
#         all_df = all_df.append(df,ignore_index=True)
#
#     all_df = all_df.sort_values(by='open_time',ascending=True)

    # print(all_df)

    # return all_df

    # for index,item in all_df.iterrows():
    #     try:
    #         dt = (pd.to_datetime(item['open_time'],unit='ms'))
    #         print(dt)
    #         dt = datetime.datetime.striptime(str(dt),'%Y-%m-%d %H:%M:%S') #2018-01-01 17:26:00
    #         print(dt)
    #
    #     except:
    #         dt = (pd.to_datatime(item['open_time'],unit='ms'))
    #         print(dt)


# def clear_dates(exchange_name,symbol):
#     df = sample_dates(exchange_name,symbol)
#
#     df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60)
#     df['Datetime'] = pd.to_datetime(df['open_time'],unit='ms') +pd.Timedelta(hours=8)
#     df['Datetime'] = df['Datetime'].apply(lambda x:str(x)[1:19])
#     df.drop_duplicates(subset=['open_time'],inplace=True)
#     df.set_index('Datetime',inplace=True)
#     print("*"*20)
#     df['ma985'] = ta.MA(df['close'],timeperiod=985)
#     df['ma610'] = ta.MA(df['close'], timeperiod=610)
#     print(df)
#     ma985 = df.iloc[-2]['ma985']
#     ma610 = df.iloc[-2]['ma610']
#     ma = df.iloc[-2]['close']
#     print(ma985)
#     print(ma610)
#     print(ma)
#
#     if ma > ma985 and ma > ma610 and ma610 > ma985:
#         binan5m.append(symbol)
#         print(f'{symbol}符合')
#     else:
#         print(f'{symbol}不符合')
#
#     print(binan5m)
#     print(f'币安5分钟985和610一共{len(binan5m)}个')
#     print("*" * 40)
#     time.sleep(2)





if __name__=='__main__':
    # jiaoyisuo = 'binance'
    # binance= ccxt.binance()
    # binance.load_markets()
    # symbols = binance.symbols
    jiaoyisuo = 'huobi'
    huobi= ccxt.huobi()
    huobi.load_markets()
    symbols = huobi.symbols



    now = int(time.time())
    last = int(now - 43200 * 60)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    end = time.localtime(now)
    start = time.localtime(last)
    end_time = time.strftime("%Y-%m-%d", end)
    start_time = time.strftime("%Y-%m-%d", start)
    print(end_time)
    print(start_time)

    # print(symbols)
    usdts = []
    for symbol in symbols:
        if symbol[-4:] == 'USDT':
            usdts.append(symbol)
    print(usdts)

    for usdt in usdts:
        try:
            crawl_exchanges_dates(jiaoyisuo, usdt, start_time, end_time)
            # sample_dates('binance', usdt)
            # clear_dates('binance', usdt)
        except (KeyError,AttributeError):
            pass
        continue
    current_path = os.getcwd()
    file_dir = os.path.join(current_path, 'binance2144.169以上5%')

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    caiji_time = time.strftime("%Y-%m-%d日%H", end)
    filename = str(caiji_time) + '点的144.169以上5%' + '.txt'
    with open(f'{file_dir}//{filename}', 'w') as f:
        f.write(str(binan4H))
    print(f'{str(caiji_time)}点采集完毕')
    # crawl_exchanges_dates('binance', 'BTC/USDT', '2021-10-3', '2021-11-3')





    # crawl_exchanges_dates('binance', 'BTC/USDT', '2021-10-3', '2021-11-3')




