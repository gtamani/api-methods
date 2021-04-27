import requests, json, os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Insert your key on this variable 
key = os.environ.get("LICHESS_KEY")

def score():
    """
    Personal Score in every mode
    """
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


def top10(mode=None):
    """
    Top 10 players in every mode
    :mode: valid arguments --> 'bullet', 'blitz', 'rapid', 'classical', 'ultraBullet', 'crazyhouse', 'chess960', 'kingOfTheHill', 'threeCheck', 'antichess', 'atomic', 'horde', 'racingKings'
    """
    header = {"Accept": "application/vnd.lichess.v3+json"}
    url= "https://lichess.org/player"
    r = requests.get(url=url,headers=header)

    if mode is not None:
        if mode in [i for i in r.json()]:
            modes = [mode]
        else:
            return "Invalid argument. Try one of these: 'bullet', 'blitz', 'rapid', 'classical', 'ultraBullet', 'crazyhouse', 'chess960', 'kingOfTheHill', 'threeCheck', 'antichess', 'atomic', 'horde', 'racingKings'"
    else:
        modes = [i for i in r.json()]

    data = {}
    index = 0

    for mode in modes:
        top = 1
        for i in r.json()[mode]:
            data[index] = {"Mode":mode,"Top":top,"Elo":i["perfs"][mode]["rating"],"Username":i["username"]}
            top +=1
            index +=1

    df = pd.DataFrame.from_dict(data,orient="index")
    return df.set_index(["Mode","Top"],drop=True)


print(top10("rapid"))