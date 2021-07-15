import requests

# No token required. 

def search(keywords):
    """
    Search an article using Wikipedia API
    """
    endpoint= "https://es.wikipedia.org/w/api.php"

    params = {
        "action":"query",
        "list":"search",
        "srprop":"snippet",
        "format":"json",
        "origin":"*",
        "utf8":"",
        "srsearch":keywords
    }
     
    r = requests.get(url=endpoint,params=params)
    text = ""
    for i in range(3):
        phrase = r.json()["query"]["search"][i]["snippet"]
        text += remove_spans(phrase)
    return text


def random_words(language="es"):
    """
    Get a random site from wikipedia
    """
    endpoint= "https://"+language+".wikipedia.org/wiki/Special:Random"
    
    r = requests.get(url=endpoint)
    content = str(r.content)
    random_search = content[content.index("<title>")+7:content.index("</title>")]
    random_search = random_search.split("-")[0]
    return random_search.replace("\\xc3\\xa9","é").replace("\\xc3\\xad","í")

def wiki(keyword,language="es"):
    """
    Search an article using Wikipedia Python's library.
    """
    import wikipedia
    wikipedia.set_lang(language)
    return wikipedia.summary(keyword,sentences=2)

def remove_spans(text):
    """
    Internal function to remove HTML tags.
    """
    
    new_text = ""
    left = text.replace("</span>","")
    while 1:
        try:
            span_init,span_finished = left.index("<span"),left.index(">") + 1
            new_text += left[:span_init]
            left = left[span_finished:]
            print(new_text)
        except ValueError:
            return new_text + left+". "

if __name__ == "__main__":
    random = random_words()
    print(search(random))
    
    