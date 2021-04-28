<h1>Pixabay API</h1>

lichess.py has the best functions either to analize your games or to create your own bot

Follow this easy steps to start using lichess API

1. Log in lichess and get the API token --> https://lichess.org/

2. Copy that token and include it in "pixabay.py"

```python
# Insert your key on this variable (line 7)
apikey = "here_include_your_key"
```


Then, you must include this file in your proyect and import pixabay functions

```python
import lichess
```
```python
from lichess import score, top10, best_move
```

<br>
<h1>Functions</h1>
<h2>Get your personal score</h2>


```python
lichess.score()
```

|   arguments	|   datatype	|   	|   default	|   observations	|   	|
|--:	|--:	|--:	|--:	|---	|---	|
|  No arguments required	|   -	|   -	|   --	|   	|   	|



<br><br>
<h2>Show the best 10 players and its ELO score</h2>


```python
lichess.top10()
```

|   arguments	|   datatype	|   	|   default	|   observations	|   	|
|--:	|--:	|--:	|--:	|---	|---	|
|  mode 	|   str	|   optional	|   None	|   valid arguments --> 'bullet', 'blitz', 'rapid','classical', 'ultraBullet', 'crazyhouse', 'chess960', 'kingOfTheHill', 'threeCheck', 'antichess', 'atomic', 'horde','racingKings' |   	|

<br><br>
<h2>Get the best move you can do with a certain board display</h2>


```python
lichess.best_move()
```

|   arguments	|   datatype	|   	|   default	|   observations	|   	|
|--:	|--:	|--:	|--:	|---	|---	|
|  fen 	|   str	|   required	|   --	|   Here's some info about FEN coding : https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation#:~:text=Forsyth%E2%80%93Edwards%20Notation%20(FEN),Scottish%20newspaper%20journalist%20David%20Forsyth. |   	|
|  depth	|   int	|   optional	|   1	|   It admits values below 10. Returns a list	|   	|
