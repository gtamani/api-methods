import requests, json, os
import pandas as pd
import numpy as np
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


def best_move(fen,depth=1):
    """
    Returns the best movement for a certain board game
    depth: 10
    """
    header = {"Authorization": "Bearer "+key}
    params = {"fen": fen}
    url = "https://lichess.org/api/cloud-eval"
    r = requests.get(url=url, headers=header,params=params)
    if r.status_code != 404:
        message = r.json()["pvs"][0]["moves"].split(" ")
        return message[:depth]


def get_fen_syntax(board, turn):
    fen = ""
    fen_notation = {1:"P",2:"R",3:"N",4:"B",5:"Q",6:"K",
                    11:"p",12:"r",13:"n",14:"b",15:"q",16:"k",
                    0:None}
    empty = 0
    for row in board:
        for letter in row:
            if fen_notation[letter] is not None:
                if empty != 0:
                    fen += str(empty)
                fen += str(fen_notation[letter])
                empty = 0
            else:
                empty += 1
        if empty != 0:
            fen += str(empty)
        empty = 0
        fen += "/"
    fen = fen[:-1]
    fen += " "+turn+" KQkq - 0 1"
    turn = "w" if turn == "b" else "b"
    return fen, turn

def move_piece(board,coord):

    letter_to_num = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}

    mfrom_column, mfrom_row = letter_to_num[coord[0]],-(int(coord[1]))
    mto_column,mto_row = letter_to_num[coord[2]],-(int(coord[3]))
    piece = int(board[mfrom_row][mfrom_column])

    if piece != 6 and piece != 16:
        board[mfrom_row][mfrom_column] = 0
        board[mto_row][mto_column] = piece

    elif piece == 6:
        if mto_column == 7: #Enroque corto
            mto_column = 6
            board[mfrom_row][mfrom_column], board[-1][-1] = 0,0
            board[mto_row][mto_column] = piece
            board[-1][5] = 2
        elif mto_column == 0: #Enroque largo
            mto_column = 2
            board[mfrom_row][mfrom_column], board[-1][0] = 0, 0
            board[mto_row][mto_column] = piece
            board[-1][3] = 2
    elif piece == 16:
        if mto_column == 7: #Enroque corto
            mto_column = 6
            board[mfrom_row][mfrom_column], board[0][-1] = 0,0
            board[mto_row][mto_column] = piece
            board[0][5] = 12
        elif mto_column == 0: #Enroque largo
            mto_column = 2
            board[mfrom_row][mfrom_column], board[0][0] = 0, 0
            board[mto_row][mto_column] = piece
            board[0][3] = 12

    print("moving from {} to {}.".format(coord[0:2], coord[2:4]))
    return board

board = np.array([[12,13,14,15,16,14,13,12,],[11]*8,[0]*8,[0]*8,[0]*8,[0]*8,[1]*8,[2,3,4,5,6,4,3,2]])

print(board)

turn= "w"
switch = True
move = 1

while switch:
    print(turn,"turn.")
    fen_board,turn = get_fen_syntax(board,turn)
    next_move= best_move(fen_board)
    if next_move is None:
        print("No more to show!")
        switch = False
    else:

        board = move_piece(board, next_move[0])
        move += 1
        print(board,"\n\n")
