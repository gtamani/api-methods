import requests
import pandas as pd
import json
from datetime import datetime

token = "bvmbb3f48v6trsjub7j0"
sandbox = "sandbox_bvmbb3f48v6trsjub7jg"



def exchange(mkt):
    """
    Muestra por pantalla todos los activos del mercado pasado como input
    US - USA
    BA - Argentina
    """
    url= "https://finnhub.io/api/v1/stock/symbol"
    params = {"token":token,"exchange":mkt}
    r = requests.get(url=url,params=params)
    df = pd.DataFrame(r.json())
    return df

def market_cap(symbol):
    """
    Devuelve la capitalización bursatil de un activo
    """
    url = "https://finnhub.io/api/v1/stock/profile2"
    params = {"token": token, "symbol": symbol}
    r = requests.get(url=url, params=params)
    return r.json()["marketCapitalization"]

def similars(symbol):
    """
    Devuelve tickers relacionados
    """
    url = "https://finnhub.io/api/v1/stock/peers"
    params = {"token": token, "symbol": symbol}
    r = requests.get(url=url, params=params)
    return r.json()

def metrics(symbol,metric = "perShare"):
    """
    Metricas de análisis Fundamental
    Valores admitidos para "metric" = ["price","valuation","growth","margin","management","financialStrength","perShare"
    """
    url = "https://finnhub.io/api/v1/stock/metric"
    params = {"token": token, "symbol": symbol,"metric":metric}
    r = requests.get(url=url, params=params)
    df = pd.DataFrame.from_dict(r.json())
    return df

def filings(symbol):
    """
    DataFrame con links de los formularios que la SEC (Security and Exchange Commission) obliga a informar
    a las empresas cotizantes
    """
    url = "https://finnhub.io/api/v1/stock/filings"
    params = {"token": token, "symbol": symbol}
    r = requests.get(url=url, params=params)
    df = pd.DataFrame.from_dict(r.json())
    return df["filingUrl"]

def ipo_calendar(toDate = "2022-01-01"):
    fromDate = datetime.today().strftime("%Y-%m-%d"),
    url = "https://finnhub.io/api/v1/calendar/ipo"
    params = {"token": token, "from": fromDate, "to": toDate}
    r = requests.get(url=url, params=params)
    df = pd.DataFrame(r.json()["ipoCalendar"])
    pd.options.display.max_columns = 10

    return df



if __name__ == "__main__":
    print(datetime.today().strftime("%Y-%m-%d"))
    print(ipo_calendar())





    #exchange("BA").to_excel("BA assets.xls")
    #print([(market_cap(i),i) for i in similars("KO")])

