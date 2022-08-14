import h5py
import datetime
import pandas as pd
import sys

START_DATE = '2012-08-13'
END_DATE = '2017-08-11'
DATE_FORMAT = '%Y-%m-%d'
START_DATETIME = datetime.datetime.strptime(START_DATE, DATE_FORMAT)

def read_stock_history(filepath):
    """ Read data from extracted h5
    Args:
        filepath: path of file
    Returns:
        history:
        abbreviation:
    """
    with h5py.File(filepath, 'r') as f:
        history = f['history'][:]
        abbreviation = f['abbreviation'][:].tolist()
        abbreviation = [abbr.decode('utf-8') for abbr in abbreviation]
    return history, abbreviation

def index_to_date(index):
    return (START_DATETIME + datetime.timedelta(index)).strftime(DATE_FORMAT)

def save_stock_data(stk,history,abbreviation):
    p=abbreviation.index(stk)
    h=history[p]
    tData=[]
    hData=['dt','sym','open','high','low','close','vol']
    for x in range(0,h.shape[0]):
        row=[]
        row.append(index_to_date(x))
        row.append(stk)
        v=h[x]
        for y in range(0,len(v)):
            row.append(v[y])
        tData.append(row)    
    df=pd.DataFrame(tData,columns=hData)
    df.set_index(pd.DatetimeIndex(df['dt']), inplace=True)
    del df['dt']
    df.to_csv(stk+".csv")
    print("store:"+stk)
    return df

stk=sys.argv[1]
history,abbreviation=read_stock_history('stocks_history_target.h5')
save_stock_data(stk,history,abbreviation)