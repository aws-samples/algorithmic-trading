import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
import backtrader.plot
import os
import pytz
from pytz import timezone
import requests
import json
import time
from algo_sim_feed import AlgoSimData

import matplotlib
import matplotlib.pyplot as plt

# More documentation about backtrader: https://www.backtrader.com/

class AlgoStrategy():
    
    def __init__(self,config,strategy):
        self.config=config
        
        self.cerebro = bt.Cerebro()        
        strategy.config=config
        strategy.init_broker(self.cerebro.broker)
        strategy.add_data(self.cerebro)
        self.cerebro.addstrategy(strategy)

        self.portfolioStartValue=self.cerebro.broker.getvalue()
                            
        self.cerebro.addanalyzer(btanalyzers.DrawDown, _name='dd')
        self.cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharpe')
        self.cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
        self.cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='ta')
        
    def performance(self):
        analyzer=self.thestrat.analyzers.ta.get_analysis()
        dd_analyzer=self.thestrat.analyzers.dd.get_analysis()
      
        #Get the results we are interested in
        total_open = analyzer.total.open
        total_closed = analyzer.total.closed
        total_won = analyzer.won.total
        total_lost = analyzer.lost.total
        win_streak = analyzer.streak.won.longest
        lose_streak = analyzer.streak.lost.longest
        pnl_net = round(analyzer.pnl.net.total,2)
        strike_rate = (total_won / total_closed) * 100
        #Designate the rows
        h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
        h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
        h3 = ['DrawDown Pct','MoneyDown', '', '']
        self.total_closed=total_closed
        self.strike_rate=strike_rate
        self.max_drawdown=dd_analyzer.max.drawdown
        r1 = [total_open, total_closed,total_won,total_lost]
        r2 = [('%.2f%%' %(strike_rate)), win_streak, lose_streak, pnl_net]
        r3 = [('%.2f%%' %(dd_analyzer.max.drawdown)), dd_analyzer.max.moneydown, '', '']
        #Check which set of headers is the longest.
        header_length = max(len(h1),len(h2),len(h3))
        #Print the rows
        print_list = [h1,r1,h2,r2,h3,r3]
        row_format ="{:<15}" * (header_length + 1)
        print("Trade Analysis Results:")
        for row in print_list:
            print(row_format.format('',*row))

        analyzer=self.thestrat.analyzers.sqn.get_analysis()
        sharpe_analyzer=self.thestrat.analyzers.sharpe.get_analysis()
        self.sqn = analyzer.sqn
        self.sharpe_ratio = sharpe_analyzer['sharperatio']
        if self.sharpe_ratio is None:
            self.sharpe_ratio=0
        self.pnl = self.cerebro.broker.getvalue()-self.portfolioStartValue
        print('[SQN:%.2f, Sharpe Ratio:%.2f, Final Portfolio:%.2f, Total PnL:%.2f]' % (self.sqn,self.sharpe_ratio,self.cerebro.broker.getvalue(),self.pnl))
        
        # plot
        chart=False
        if 'chart' in self.config and self.config['chart']=='true':
            chart=True
        if chart:
            fig=self.cerebro.plot()
            plt.rcParams["figure.figsize"] = [16,9]
            plt.savefig(os.path.join(StrategyTemplate.MODEL_PATH, 'chart.png'))
    
    def submit(self):
        try:
            if 'submitUrl' in self.config:
                name=self.config['user']+'@'+self.config['account']
                algo=self.config['algo_name']
                submitUrl=self.config['submitUrl']

                URL = submitUrl
                ts=str(int(time.time()))       
                PARAMS={'id': algo,
                        'name': name,
                        'trades': self.total_closed,
                        'strike_rate': self.strike_rate,
                        'max_drawdown': self.max_drawdown, 
                        'pnl': self.pnl,
                        'sqn': self.sqn,
                        'sharpe_ratio': self.sharpe_ratio}
                print("submit:%s" % (json.dumps(PARAMS)))
                r = requests.get(url = URL, params = PARAMS, timeout=3) 
                print("status=%s,res=%s" % (r.status_code,r.text))
                if r.status_code == 200:
                    print("performance submitted")
                else:
                    print("error submitting performance:%s" % r.text)
        except Exception as e:
            print("error submitting performance:%s" % e)
        
    def run(self):
        thestrats = self.cerebro.run()
        self.thestrat = thestrats[0]
        self.performance()
        self.submit()

class StrategyTemplate(bt.Strategy):

    PREFIX='/opt/ml/'
    TRAIN_FILE = os.path.join(PREFIX,'input/data/training/data.csv')
    CONFIG_FILE = os.path.join(PREFIX,'input/config/hyperparameters.json')
    MODEL_PATH = os.path.join(PREFIX,'model')
    
    def __init__(self):         
        with open(StrategyTemplate.CONFIG_FILE, 'r') as f:
            self.config = json.load(f)
        print("[INIT]:config:%s=%s" % (StrategyTemplate.CONFIG_FILE,self.config))
        
        self.lastDay=-1
        self.lastMonth=-1
        self.dataclose = self.datas[0].close
    
    @staticmethod
    def init_broker(broker):
        pass
    
    @staticmethod
    def add_data(cerebro):
        pass
        
    def notify_order(self, order):
        dt=self.datas[0].datetime.datetime(0)
       
        if order.status in [order.Completed]:
            if order.isbuy():
                print(
                    '[%s] BUY EXECUTED, Price: %.2f, PNL: %.2f, Cash: %.2f' %
                         (dt,order.executed.price,order.executed.pnl,self.broker.getvalue()))
            else:  # Sell
                print('[%s] SELL EXECUTED, Price: %.2f, PNL: %.2f, Cash: %.2f' %
                         (dt,order.executed.price,order.executed.pnl,self.broker.getvalue()))
                
    def next(self):
        dt=self.datas[0].datetime.datetime(0)
        #print("[NEXT]:%s:close=%s" % (dt,self.dataclose[0]))
        
        #SOM
        if self.lastMonth!=dt.month:
            if self.lastMonth!=-1:
                chg=self.broker.getvalue()-self.monthCash
                #print("[%s] SOM:chg=%.2f,cash=%.2f" % (dt,chg,self.broker.getvalue()))
            self.lastMonth=dt.month
            self.monthCash=self.broker.getvalue()
        
        #SOD
        if self.lastDay!=dt.day:
            self.lastDay=dt.day
            #print("[%s] SOD:cash=%.2f" % (dt,self.broker.getvalue()))
