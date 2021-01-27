import requests,json
import datetime
import pandas as pd

"""
Definir todo como una clase
"""

def getToken():
    """
    Establece conexión con la API-REST de InvertirOnline
    """

    url = "https://api.invertironline.com/token"

    user = input("User: ")
    password = input("Password: ")

    data = {"username":user,
            "password":password,
            "grant_type":"password"}

    r = requests.post(url=url, data=data)
    access = json.loads(r.text)

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

    data = json.loads(r.text)

    data = {"instrument" : instrumento,
            "price" : data["ultimoPrecio"],
            "cantBid" : int(data["puntas"][0]["cantidadCompra"]),
            "Bid": data["puntas"][0]["precioCompra"],
            "Ask": data["puntas"][0]["precioVenta"],
            "cantAsk": int(data["puntas"][0]["cantidadVenta"])}
    print(data)
    return data


if __name__ == "__main__":
    expires_in = None

    """
    mep = local["Ask"]/especieD["Bid"] COMPRA MEP PUNTAS
    mep = (local["Ask"]*(1+cometa))/(especieD["Bid"]*(1-cometa)) COMPRA MEP PUNTAS CON COMISION
    mep = local["price"]/especieD["price"] COMPRA MEP LAST PRICE
    
    op1 = Operación 1 - Compro bono A en pesos.
    op2 = Operación 2 - Vendo bono A en dolares.
    op3 = Operación 3 - Vendo bono B en dolares.
    op4 = Operación 4 - Compro bono A en pesos.
    
    """

    op1,op2,op3,op4,mepBarato,mepCaro = None,None,None,None,None,None
    cometa = 0.005

    for i in ["AL29","AL30","AL35","AE38","AL41"]:
        local = getPrices(i)
        especieD = getPrices(i+"D")

        mepC = round((local["Ask"]/especieD["Bid"]),2)
        mepV = round((local["Bid"]/especieD["Ask"]),2)

        if mepBarato is None or mepC < mepBarato:
            mepBarato = mepC
            op1,op2 = local["Ask"],especieD["Bid"]
        if mepCaro is None or mepV > mepCaro:
            mepCaro = mepV
            op3,op4 = local["Bid"],especieD["Ask"]

        print("mep barato: ",mepBarato," - mep caro: ",mepCaro)

        comision = local["Ask"]*cometa
        comision2 = especieD["Bid"]*cometa
        mep = round(local["price"]/especieD["price"],2)

        print(i," MEP: ",mep," - MEP COMPRA: ",mepC," - MEP VENTA: ",mepV,"      $",comision," USD",comision2)

    disponible_pesos = 100000
    print()
    print(op1,op2,op3,op4)

    op1 *= 1+cometa
    op4 *= 1+cometa
    op2 *= 1-cometa
    op3 *= 1-cometa

    print(op1,op2,op3,op4)

    cantop1 = int(disponible_pesos/op1)


    

    df = pd.DataFrame(columns=["Precio","Cantidad","Resto"])
    df.loc["1. Compro A en pesos"] = [op1,cantop1,disponible_pesos-(op1*cantop1)]