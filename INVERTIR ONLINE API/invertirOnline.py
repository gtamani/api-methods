import requests,json
import datetime,os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

"""
Load your credentials on line 20 and 21
"""

def getToken():
    """
    Establece conexión con la API-REST de InvertirOnline
    """

    url = "https://api.invertironline.com/token"

    # Insert your credentials on these variables 
    user = os.environ.get("INVERTIR_ONLINE_USER")
    password = os.environ.get("INVERTIR_ONLINE_PASSWORD")

    data = {"username":user,
            "password":password,
            "grant_type":"password"}

    r = requests.post(url=url, data=data)
    access = json.loads(r.text)

    print()
    return access["access_token"], datetime.datetime.strptime(access[".expires"],"%a, %d %b %Y %H:%M:%S GMT")

def isTokenAvailable():
    global token,expires_in
    if expires_in is None or expires_in - datetime.datetime.now()>datetime.timedelta(seconds=10) is False:
        token,expires_in = getToken()

def getPrices(instrumento="AL29D"):
    isTokenAvailable()

    headers = {"Authorization": "Bearer " + token}

    r = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/"+instrumento+"/Cotizacion",
                      headers= headers)

    data = {"instrument": instrumento,
            "price": None,
            "cantBid": None,
            "Bid": None,
            "Ask": None,
            "cantAsk": None}

    if str(r.content) != "b''": # Si el json no viene vacío...
        jsonloads = json.loads(r.text)

        data["price"] = jsonloads["ultimoPrecio"]
        data["cantBid"] = int(jsonloads["puntas"][0]["cantidadCompra"])
        data["Bid"] = jsonloads["puntas"][0]["precioCompra"]
        data["Ask"] = jsonloads["puntas"][0]["precioVenta"]
        data["cantAsk"] = int(jsonloads["puntas"][0]["cantidadVenta"])

    return data




if __name__ == "__main__":
    """
    Bot que detecta oportunidades de arbitraje en MEP de bonos y CEDEARS
    """

    expires_in = None
    op1,op2,op3,op4,mepBarato,mepCaro,a,b = None,None,None,None,None,None,None,None
    cometa = 0.005
    disponible_pesos, disponible_dolares = 100000, 0
    inicio = 100000

    #equity = ["AL29", "AL30", "AL35", "AE38", "AL41", "AAPL", "AMZN", "DISN", "INTC", "KO", "MELI"]
    equity = ["AL29","AL30"]

    for i in equity:
        local = getPrices(i)
        especieD = getPrices(i+"D")

        try:
            if local["Ask"] != 0:
                mepC = round((local["Ask"]/especieD["Bid"]),2)
        except:
            mepC = None

        try:
            mepV = round((local["Bid"] / especieD["Ask"]), 2)
        except:
            mepV = None

        try:
            lastMep = round(local["price"] / especieD["price"], 2)
        except:
            lastMep = None


        if mepC is not None and (mepBarato is None or mepC < mepBarato):
            mepBarato = mepC
            op1,op2 = local["Ask"],especieD["Bid"]
            a = local["instrument"]
        if mepV is not None and (mepCaro is None or mepV > mepCaro):
            mepCaro = mepV
            op3,op4 = especieD["Bid"],local["Ask"]
            b = local["instrument"]


        #print("mep barato: ",mepBarato," - mep caro: ",mepCaro)
        #print(i,"LAST MEP: ",lastMep," - MEP COMPRA: ",mepC," - MEP VENTA: ",mepV,"      $")
        #print()


    print()

    #print(op1,op2,op3,op4)

    op1 *= 1+cometa
    op4 *= 1-cometa
    op2 *= 1-cometa
    op3 *= 1+cometa

    #print(op1,op2,op3,op4)

    cantop1 = int(disponible_pesos/op1)

    print()

    df = pd.DataFrame(columns=["Precio","Cantidad","Pesos","Dolares"])
    df.loc["0. Inicio"] = [0,0,disponible_pesos,disponible_dolares]

    disponible_pesos -= (op1 * cantop1)

    df.loc["1. Compro "+a] = [op1,cantop1,disponible_pesos,0]

    disponible_dolares += cantop1*op2

    df.loc["2. Vendo "+a+"D"] = [op2,cantop1,disponible_pesos,disponible_dolares]

    cantop3 = int(disponible_dolares / op3)
    disponible_dolares -= op3 * cantop3

    df.loc["3. Compro "+b+"D"] = [op3,cantop3,disponible_pesos,disponible_dolares]

    disponible_pesos += cantop3 * op4

    df.loc["4. Vendo "+b] = [op4,cantop3,disponible_pesos,disponible_dolares]

    resultado = disponible_pesos + disponible_dolares * mepBarato

    if resultado > inicio:
        print(df)
        print()
        print("Obtengo: $", round(resultado,2))
        print("Ganancia: $", round(resultado-inicio,2))
        print("Resultado arbitraje: %", round(((resultado/inicio)-1)*100,2))
    else:
        print("Por el momento, no hay oportunidades de arbitraje.")


