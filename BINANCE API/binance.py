import requests, pandas as pd,datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

# Insert your key on this variable 
key = os.environ.get("BINANCE_KEY")


def getInfo():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    r = requests.get(url=url)
    return pd.DataFrame(r.json()["symbols"])

def getBook(symbol):
    url = "https://api.binance.com/api/v3/depth"
    params = {"symbol":symbol}
    r = requests.get(url=url,params=params)
    print(r.json())

def lastTrades(symbol,limit=1000):
    """
    Info sobre los últimos n trades (precio, cantidad,etc)
    """
    url = "https://api.binance.com/api/v3/trades"
    params = {"symbol": symbol,"limit":limit}
    r = requests.get(url=url, params=params)
    df = pd.DataFrame(r.json())

    df.time = pd.to_datetime(df.time)
    df.set_index(df.time,inplace=True)

    to_num = ["price","qty","quoteQty"]
    df.loc[:,to_num] = df.loc[:,to_num].apply(pd.to_numeric)
    return df

def historicalTrades(symbol,fromId=None,limit=None):
    """
    Precios históricos
    :param fromId: desde Id
    :param limit: número de datos
    :return: df
    """
    url = "https://api.binance.com/api/v3/historicalTrades"
    headers = {"X-MBX-APIKEY" : key}
    params = {"symbol": symbol, "limit": limit, "fromId":fromId}


    r = requests.get(url=url, params=params,headers=headers)

    df = pd.DataFrame(r.json())
    return df

def historical(symbol,interval,since=None,to=None,limit=1000):
    """

    :param symbol:
    :param interval: admitted = ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1M"]
    :param since:
    :param to:
    :param limit:
    :return:
    """
    url = "https://api.binance.com/api/v3/klines"
    headers = {"X-MBX-APIKEY": key}
    params = {"symbol": symbol, "interval": interval, "startTime": since, "endTime": to, "limit": limit}
    r = requests.get(url=url, params=params, headers=headers)

    columns = ["openTime","Open","High","Low","Close","Volume","cTime","qVolume","trades","takerBase","takerQuote","Ignore"]
    df = pd.DataFrame(r.json(),columns=columns)
    return df

def timestamp(year,month,day):
    return int(dt.datetime.timestamp(dt.datetime(year,month,day)))*1000


if __name__ == "__main__":
    #historical("BTCUSDT","1m",1610296965000)
    pass







