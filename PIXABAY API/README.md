<h1>Pixabay API</h1>

pixabay.py allows you to download on your computer either photos or videos from the most popular web of free high definition content!

Follow this easy steps to start using pixabay API

1. Log in pixabay  and get the API token --> https://pixabay.com/api/docs/

2. Copy that token and include it in "pixabayToken.txt"


Then, you must include this file in your proyect and import pixabay functions

```python
import pixabay
```
```python
from pixabay import downloadImg, downloadVideos
```

<br><br>
<h1>Functions</h1>
<h2>Download Images</h2>


```python
pixabay.downloadImg("beer")
```

|   arguments	|   datatype	|   	|   default	|   observations	|   	|
|--:	|--:	|--:	|--:	|---	|---	|
|  keyWords 	|   str	|   required	|   --	|   	|   	|
|  quantity 	|   int	|   optional	|   1	|   max 20 fotos	|   	|


<br><br>
<h2>Download Videos</h2>


```python
pixabay.downloadVideo("people working")
```

|   arguments	|   datatype	|   	|   default	|   observations	|   	|
|--:	|--:	|--:	|--:	|---	|---	|
|  keyWords 	|   str	|   required	|   --	|   	|   	|
|  quantity 	|   int	|   optional	|   1	|   max 20 videos	|   	|
|  quality 	|   int	|   optional	|   4	|   It admites values from 0 (worst) to 4 (best) resolution	|   	|