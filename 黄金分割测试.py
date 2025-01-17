#-*- codeing = utf-8 -*-


import pandas as pd
import time
import os
import datetime
import ccxt
import talib as ta
binan4Hk = []
binan4Hv = []
hhd5 = []
h768u5 = []
h768d5 = []
h618u5 = []
h618d5 = []
h50u5 = []
h50d5 = []
h382u5 = []
h382d5 = []
h236u5 = []
h236d5 = []
llu5 = []

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
        start_time_stamp = int(time.mktime(start_time.timetuple())) * 1000
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

        df['slowk'], df['slowd'] = ta.STOCH(
            df['high'].values,
            df['low'].values,
            df['close'].values,
            fastk_period=9,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0)
        # 求出J值，J = (3*K)-(2*D)
        df['slowj'] = list(map(lambda x, y: 3 * x - 2 * y, df['slowk'], df['slowd']))

        # print(df['slowk'], df['slowd'], df['slowj'])

        df['cci'] = ta.CCI(df['high'].values, df['low'].values, df['close'].values, timeperiod=14)

        df['hh'] = ta.stream_MAX(df['high'],timeperiod=210)
        df['ll'] = ta.stream_MIN(df['low'], timeperiod=210)


        # exit()
        print(df)

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
        mahigh = df.iloc[-2]['high']
        malow = df.iloc[-2]['low']
        k = df.iloc[-2]['slowk']
        d = df.iloc[-2]['slowd']
        j = df.iloc[-2]['slowj']
        cci = df.iloc[-2]['cci']
        hh = df.iloc[-4]['hh']
        ll = df.iloc[-4]['ll']
        print(f'210周期内最高点是{hh}')
        print(f'210周期内最低点是{ll}')
        return x1,x2,x3,x4,x5,x6,x7,x8,maclose,maopen,mahigh,malow,k,d,j,cci,hh,ll

    except:
        print(f"{symbol}数据请求错误，跳过")
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

            hma5, hma10, hma20, hma30, hma60, hma90, hma144, hma169, hmaclose, hmaopen, hmahigh, hmalow, k, d, j,cci, hh, ll = crawl_exchanges_dates('binance', usdt, '1d', 5, 6, 7, 8, 9, 10, 11, 210, 1440)
            # hma16905 = float(hma169) + float(hma169) * 0.05
            # hmacloseup = hmaclose + hmaclose * 0.05
            # hmaclosedown = hmaclose - hmaclose * 0.05
            # ABS(C - O) < 0.02 AND H - C > 0.03 AND C - L > 0.03;
            #hh
            if hma5 is None:
                continue
            h786 = hh - (hh - ll) * (1-0.786) #
            h618 = hh - (hh - ll) * (1-0.618)
            h50 = hh - (hh - ll) * (1-0.5)
            h382 = hh - (hh - ll) * (1-0.382)
            h236 = hh - (hh - ll) * (1-0.236)
            # ll
            # h6 = hh + (hh - ll) * 0.382
            # h7 = hh + (hh - ll) * 0.618
            # print(h1)
            # print(h2)
            # print(h3)
            # print(h4)
            # print(h5)
            # print(h6)
            # print(h7)
            """
            顶1:=HH+(HH-LL)*0.191;
            顶2:=HH+(HH-LL)*0.382;
            顶3:=HH+(HH-LL)*0.618;
            底1:=IF((HH-LL)<LL,LL-(HH-LL)*0.191,LL-LL*0.191);
            底2:=IF((HH-LL)<LL,LL-(HH-LL)*0.382,LL-LL*0.382);
            底3:=IF((HH-LL)<LL,LL-(HH-LL)*0.618,LL-LL*0.618);
            """






            if (hh - hh*0.05) < hmaclose < hh:

                hhd5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合最高点以下百分之五')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)
            elif h786 < hmaclose < (h786 + h786 * 0.05):

                h768u5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h768u5百分之五')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif (h786 - h786 * 0.05) < hmaclose < h786:

                h768d5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h768d5百分之五')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif h618 < hmaclose < (h618 + h618 * 0.05):

                h618u5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h618u5百分之五')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif (h618 - h618 * 0.05) < hmaclose < h618:

                h618d5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h618d5百分之五')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif h50 < hmaclose < (h50 + h50 * 0.05):

                h50u5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h50u5')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif (h50 - h50 * 0.05) < hmaclose < h50:

                h50d5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h50d5')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif h382 < hmaclose < (h382 + h382 * 0.05):

                h382u5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h382u5')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif (h382 - h382 * 0.05) < hmaclose < h382:

                h382d5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h382d5')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif h236 < hmaclose < (h236 + h236 * 0.05):

                h236u5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h236u5')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif (h236 - h236 * 0.05) < hmaclose < h236:

                h236d5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合h236d5')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)

            elif ll < hmaclose < (ll + ll * 0.05):

                llu5.append(usdt)
                binan4Hv.append(hmaclose)
                print(f'{usdt}符合llu5')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                print("*" * 40)




            else:

                print(f'{usdt}不符合')
                print(f'hhd5={hhd5}')
                print(f'hhd5一共{len(hhd5)}个')
                print(f'h768u5={h768u5}')
                print(f'h768u5一共{len(h768u5)}个')
                print(f'h768d5={h768d5}')
                print(f'h768d5一共{len(h768d5)}个')
                print(f'h618u5={h618u5}')
                print(f'h618u5一共{len(h618u5)}个')
                print(f'h618d5={h618d5}')
                print(f'h618d5一共{len(h618d5)}个')
                print(f'h50u5={h50u5}')
                print(f'h50u5一共{len(h50u5)}个')
                print(f'h50d5={h50d5}')
                print(f'h50d5一共{len(h50d5)}个')
                print(f'h382u5={h382u5}')
                print(f'h382u5一共{len(h382u5)}个')
                print(f'h382d5={h382d5}')
                print(f'h382d5一共{len(h382d5)}个')
                print(f'h236u5={h236u5}')
                print(f'h236u5一共{len(h236u5)}个')
                print(f'h236d5={h236d5}')
                print(f'h236d5一共{len(h236d5)}个')
                print(f'llu5={llu5}')
                print(f'llu5一共{len(llu5)}个')
                # print(binan4Hk)
                # print(f'币安4小时CCI小于-200一共{len(binan4Hk)}个')
                print("*" * 40)

        except (KeyError,TypeError):
            pass
        continue


    current_path = os.getcwd()
    file_dir = os.path.join(current_path,'币安1日黄金分割测试')

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    now = int(time.time())
    # last = int(now - 403200 * 60)
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    end = time.localtime(now)
    caiji_time = time.strftime("%Y-%m-%d日%H", end)
    filename = str(caiji_time) + '币安1日黄金分割测试测试所有币' + '.txt'
    with open(f'{file_dir}//{filename}', 'w') as f:
        f.write(str(hhd5))

    filename1 = str(caiji_time) + '币安1日黄金分割测试收盘价格' + '.txt'
    with open(f'{file_dir}//{filename1}', 'w') as f1:
        f1.write(str(binan4Hv))
    print(f'{str(caiji_time)}点采集完毕')



