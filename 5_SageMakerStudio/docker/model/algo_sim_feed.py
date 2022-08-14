import datetime
import struct
import time

from backtrader.feed import DataBase
from backtrader import date2num
from backtrader import TimeFrame
import backtrader as bt

import numpy as np
import pandas as pd

# Based on this: https://towardsdatascience.com/simulating-stock-prices-in-python-using-geometric-brownian-motion-8dfd6e8c6b18

class AlgoSimData(DataBase):
    def __init__(self,datafile):
        super(AlgoSimData, self).__init__()

        df = pd.read_csv(datafile,infer_datetime_format=True, parse_dates=['dt'])
       
        start_date = '2012-08-13'
        end_date = '2017-08-11'
        
        now = datetime.datetime.now() # current date and time
        pred_end_date = now.strftime("%Y-%m-%d")
        
        self.fromdate=pd.to_datetime(end_date, format = "%Y-%m-%d")
        self.todate=pd.to_datetime(pred_end_date, format = "%Y-%m-%d")
        self.timeframe=bt.TimeFrame.Days

        S_eon = df[["dt","close"]]

        returns = (S_eon.loc[1:, 'close'] - \
                   S_eon.shift(1).loc[1:, 'close']) / \
                   S_eon.shift(1).loc[1:, 'close']

        # Parameter Assignments
        So = S_eon.loc[S_eon.shape[0] - 1, "close"]
        dt = 1 # day   # User input
        n_of_wkdays = pd.date_range(start = pd.to_datetime(end_date, 
                         format = "%Y-%m-%d") + pd.Timedelta('1 days'), 
                         end = pd.to_datetime(pred_end_date, 
                         format = "%Y-%m-%d")).to_series().map(lambda x: 
                         1 if x.isoweekday() in range(1,6) else 0).sum()
        T = n_of_wkdays # days  # User input -> follows from pred_end_date
        N = T / dt
        t = np.arange(1, int(N) + 1)
        mu = np.mean(returns)
        sigma = np.std(returns)
        scen_size = 1 # User input
        b = {str(scen): np.random.normal(0, 1, int(N)) for scen in range(1, scen_size + 1)}
        W = {str(scen): b[str(scen)].cumsum() for scen in range(1, scen_size + 1)}

        # Calculating drift and diffusion components
        drift = (mu - 0.5 * sigma**2) * t
        diffusion = {str(scen): sigma * W[str(scen)] for scen in range(1, scen_size + 1)}

        # Making the predictions
        S = np.array([So * np.exp(drift + diffusion[str(scen)]) for scen in range(1, scen_size + 1)]) 
        S = np.hstack((np.array([[So] for scen in range(scen_size)]), S)) # add So to the beginning series

        # Dataframe format for predictions - first 10 scenarios only
        self.df = pd.DataFrame(S.swapaxes(0, 1)[:, :10]).set_index(
                   pd.date_range(start = S_eon["dt"].max(), 
                   end = pred_end_date, freq = 'D').map(lambda x:
                   x if x.isoweekday() in range(1, 6) else np.nan).dropna()
                   ).reset_index(drop = False)
        print("SimData generated:from=%s,to=%s,count=%s" % (self.fromdate,self.todate,len(self.df)))
        self.n=0
 
    def start(self):
        print("start feed")

    def stop(self):
        print("stop feed")

    def _load(self):
        #print("load feed")
        if self.n>=len(self.df):
            return False
        
        v=self.df.values
        #print(v)
        #print(self.n)
        dt=v[self.n][0]
        close=v[self.n][1]
        #print("%s:%s:%s" % (self.n,dt,close))
        
        self.lines.datetime[0] = date2num(dt)
        
        print(self.num2date(self.lines.datetime[0]))
        
        self.lines.open[0] = close
        self.lines.high[0] = close
        self.lines.low[0] = close
        self.lines.close[0] = close
        self.lines.volume[0] = 0
        
        self.n=self.n+1
        return True