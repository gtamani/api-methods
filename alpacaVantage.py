import requests, pandas as pd

def get_intra(symbol,interval = "15min"):
    """
    DataFrame con datos OHCL intradiarios. Frecuencias admitidas: 1min, 5min, 15min, 30min, 60min
    """
    params = {"function": "TIME_SERIES_INTRADAY","symbol": symbol,"interval": interval ,"apikey":"YELY5RODQVJZX36J"}
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)
    data = r.json()["Time Series ("+interval+")"]

    return set_df(data)


def get_daily(symbol,extended = False):
    """
    DataFrame con datos OHCL. No ajustado por dividendos
    """
    if extended:
        outputsize = "full"
    else:
        outputsize = "compact"
    params = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "apikey": "YELY5RODQVJZX36J",
              "outputsize":outputsize}
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)
    data = r.json()["Time Series (Daily)"]
    return set_df(data)


def set_df(data):
    """
    Seteo de DataFrames
    """
    df = pd.DataFrame.from_dict(data, orient="index")
    df.index.name, df.columns = "Date", ["Open", "High", "Low", "Close", "Volume"]
    df = df.astype("float")
    df = df.sort_values("Date", ascending=True)
    df.index = pd.to_datetime(df.index)
    return df

def get_dailyAdj(symbol):
    """
    Devuelve un DataFrame con la serie histórica de un activo, OHCL, Close Adjusted, Dividends, Splits
    """
    params = {"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": symbol, "apikey": "YELY5RODQVJZX36J",
              "outputsize": "full"}
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)
    data = r.json()["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(data,orient="index").astype("float")
    df.index.name, df.columns = "Date", ["Open", "High", "Low", "Close", "Adj Close", "Volume", "Div", "Split"]
    df = df.sort_values("Date", ascending=True)
    df.index = pd.to_datetime(df.index)
    return df

def get_splits(symbol):
    """
    Devuelve los últimos splits de un activo
    """
    df = get_dailyAdj(symbol)
    return df.loc[df.Split != 1]

def get_dividends(symbol):
    """
    Devuelve los últimos pagos de dividendos de un activo
    """
    df = get_dailyAdj(symbol)
    return df.loc[df.Div != 0]

def search(keyword):
    """
    Buscador de activos por palabras claves
    """
    params = {"function": "SYMBOL_SEARCH", "keywords": keyword, "apikey": "YELY5RODQVJZX36J"}
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)
    data = r.json()["bestMatches"]
    for i in data:
        print("{:13} - {} ({})".format(i["1. symbol"],i["2. name"],i["4. region"]))

def last_price(symbol):
    """
    Último precio de un activo
    """
    params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": "YELY5RODQVJZX36J"}
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)
    return float((r.json()["Global Quote"]["05. price"]))


def fx(curr1,curr2):
    """
    Devuelve la relación de dos pares de monedas
    """
    params = {"function": "CURRENCY_EXCHANGE_RATE", "from_currency": curr1, "to_currency": curr2, "apikey": "YELY5RODQVJZX36J"}
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)
    return round(float(r.json()['Realtime Currency Exchange Rate']["5. Exchange Rate"]),2)


def crypto_rate(symbol):
    """
    Devuelve el rating FCAS (Fundamental Crypto Asset Score)
    """
    params = {"function": "CRYPTO_RATING", "symbol": symbol, "apikey": "YELY5RODQVJZX36J"}
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)
    return int(r.json()["Crypto Rating (FCAS)"]['4. fcas score'])

def ema(symbol,time_period,last = True,series_type = "close",interval="daily"):
    """
    Media Móvil Exponencial

    :param last: True devuelve la EMA para la última cotización, False devuelve EMA para una serie historica
    :param time_period: Frecuencia de la media móvil
    :param series_type: Datos tomados para el cálculo del indicador ("close","open","high","low"
    :param interval: Número de datapoints. Solo integers
    """
    params = {"function": "EMA", "symbol": symbol, "interval": interval, "apikey": "YELY5RODQVJZX36J",
              "time_period": time_period, "series_type": series_type }
    url = "https://www.alphavantage.co/query"
    r = requests.get(url=url, params=params)

    if last:
        return float(r.json()['Technical Analysis: EMA'][r.json()['Meta Data']['3: Last Refreshed']]["EMA"])
    else:
        data = r.json()['Technical Analysis: EMA']
        df = pd.DataFrame.from_dict(data,orient="index")
        df.index.name = "Date"
        df.index = pd.to_datetime(df.index)
        return df

def macd(symbol,series_type="close"):
    """
    Indicador técnico de convergencia/divergencia de las medias móviles.
    Devuelve las dos lineas del MACD junto al histograma sobre una serie historica de un activo pasado como input.
    """
    url= "https://www.alphavantage.co/query"
    params = {"function":"MACD","symbol":symbol,"interval":"daily","series_type":series_type,
              "apikey":"YELY5RODQVJZX36J"}
    r = requests.get(url=url,params=params)
    df = pd.DataFrame.from_dict(r.json()["Technical Analysis: MACD"])
    df = df.T #matriz transpuesta
    df = df.rename(columns={"MACD_Hist":"Histograma","MACD_Signal":"MACD señal"})
    df.index.name = "Date"
    df.index = pd.to_datetime(df.index)
    df = df.astype("float")
    df = df.sort_values("Date",ascending=True)
    return df

def rsi(symbol,series_type="close",time_period=60):
    """
    Relative Strenght Index (Índice de fuerza relativa)
    """
    url = "https://www.alphavantage.co/query"
    params = {"function": "RSI", "symbol": symbol, "interval": "daily", "series_type": series_type,
              "apikey": "YELY5RODQVJZX36J", "time_period":time_period}
    r = requests.get(url=url, params=params)
    df = pd.DataFrame.from_dict(r.json()["Technical Analysis: RSI"],orient="index")
    df.index.name = "Date"
    df = df.astype("float")
    df.index = pd.to_datetime(df.index)
    return df


