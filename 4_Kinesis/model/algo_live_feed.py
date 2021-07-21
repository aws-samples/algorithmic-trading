import datetime
import struct
import time

from backtrader.feed import DataBase
from backtrader import date2num
from backtrader import TimeFrame
import backtrader as bt
import math
import numpy as np
import pandas as pd
import json
import boto3

class AlgoLiveData(DataBase):
    def __init__(self,region):
        super(AlgoLiveData, self).__init__()
        self.region=region
        self.lambda_client = boto3.client('lambda',region_name=self.region)
        self.connected=False

        #start_date = '2017-08-11'
        #now = datetime.datetime.now() # current date and time
        #end_date = now.strftime("%Y-%m-%d")
        
        #self.fromdate=pd.to_datetime(start_date, format = "%Y-%m-%d")
        #self.todate=pd.to_datetime(end_date, format = "%Y-%m-%d")
        self.timeframe=bt.TimeFrame.Ticks
        print(self.lines.datetime.array)
 
    def start(self):
        print("start feed")
        print(self.lines.datetime.array)
    
    def stop(self):
        print("stop feed")
    
    def islive(self):
        '''Returns ``True`` to notify ``Cerebro`` that preloading and runonce
        should be deactivated'''
        return True
 
    def haslivedata(self):
        '''Returns ``True`` to notify ``Cerebro`` that preloading and runonce
        should be deactivated'''
        return self.connected

    def _load(self):
        #print("A:%s" % self.lines.datetime.array)
        if not self.connected:
            while not self.connected:
                self.pull()
        else:
            self.pull()
        return True

    def pull(self):
        #print("B:%s" % self.lines.datetime.array)
        if math.isnan(self.lines.datetime[0]):
            now = datetime.datetime.now()
            self.lines.datetime[0]=date2num(now)
        now=datetime.datetime.now()
        try:
            item={}
            res=self.lambda_client.invoke(
                FunctionName='algo_market_data',
                InvocationType='RequestResponse',
                Payload=json.dumps(item)
            )
            t=res['Payload']
            l=json.loads(t.read().decode('utf-8'))
            print("load:%s" % l)
            
            #print(self.lines.datetime.array)
            #print(self.lines.close.array)
            
            for x in l:
                dt=pd.to_datetime(x['date'], format = "%Y-%m-%d")
                #print(dt)
                close=x['close']
                
                self.lines.datetime[0] = date2num(datetime.datetime.now())
                self.lines.open[0] = close
                self.lines.high[0] = close
                self.lines.low[0] = close
                self.lines.close[0] = close
                self.lines.volume[0] = 0
                
                self.connected=True
                self._laststatus=self.LIVE
                #print("connected")
        except Exception as e:
            print("err:%s" % e)
            time.sleep(5)