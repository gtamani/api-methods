import requests,json
import pandas as pd

def getKey():
    with open("lichessToken.txt","r") as handler:
        return str(handler.read())

def score():
    key = getKey()
    header = {"Authorization": "Bearer "+key}
    url= "https://lichess.org/api/account"
    r = requests.get(url=url,headers=header)
    r = r.json()["perfs"]
    data = {}

    for i in r:
        print(i,r[i]["games"],r[i]["rating"])
        data[i] = [r[i]["games"],r[i]["rating"]]
    
    df = pd.DataFrame.from_dict(data,orient="index")
    df.columns = ["Games Played","Rating"]
    return df


def top10():
    key = getKey()
    header = {"Accept": "application/vnd.lichess.v3+json"}
    url= "https://lichess.org/player"
    r = requests.get(url=url,headers=header)
    modes = [i for i in r.json()]
    r = r.json()["bullet"]
    print(r)

    data = {}
    for mode in range(len(modes)):
        print(mode,modes[mode])
        data[str(mode+1)] = {}

        for i in r:
            data[str(mode+1)]["username"] = i["username"]
            data[str(mode+1)]["rating"] = i["perfs"]["bullet"]["rating"]
    print(data)
    df = pd.DataFrame.from_dict(data,orient="index")
    print(df)
            
        

top10()
