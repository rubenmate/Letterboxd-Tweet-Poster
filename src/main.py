# TODO: Postear listas en otro hilo diferente
# TODO: Ir guardando en una lista items posteados para no repetirlo

#Importaciones: Tweepy para la API de Twitter y Feedparser para el feed RSS
import feedparser
import time
import json
import emoji

from config import create_api

firstTime = True

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    firstTime = config["firstTime"]
except Exception as e:
    print (e)

if firstTime:
    config = {"firstTime": False, "last_tweet": 1376990746084007941, "index": 1, "previous_film": ""}
    with open('config.json', 'w') as f:
        json.dump(config, f)

api = create_api()

url = 'https://letterboxd.com/rbnmustdie/rss/'
last_tweet = api.get_status(config["last_tweet"])
index = config["index"]
previous_film = config["previous_film"]


def letterboxd_rss():
    films_list = []
    lists = []
    try:
        feed = feedparser.parse(url)

        entries = feed.entries
        for e in entries:

            title = e.title
            link = e.link
            published = e.published

            if "/list/" in link:
                list = {
                    'title': title,
                    'link': link,
                    'published': published
                }
                lists.append(list)
            else:
                film = {
                    'title': title,
                    'link': link,
                    'published': published
                }
                films_list.append(film)

        return films_list, lists
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)

while True:
    print(index)
    print('Starting scraping')

    films_raw_data, lists_raw_data = letterboxd_rss()

    tweet_string = ""
    f = films_raw_data[0]

    if f != previous_film:
        print(f)
        previous_film = f
        emoji_star = emoji.emojize(":star:")
        star = u"\u2605"
        # FIXME: Arreglar replace y comprimir código haciendo más legible la línea
        tweet_string = str(index) + ".- " + str(f['title']).replace(star, emoji_star, -1)+'\n' + str(f['link']).replace('(','',-1).replace(')','',-1).replace(',','',-1).replace('\'','',-1) +'\n'
        print(tweet_string)
        try:
            last_tweet = api.update_status(tweet_string, last_tweet.id)
            index += 1
            print("Posted tweet with id:", last_tweet.id)
        except Exception as e:
            print("Failed posting tweet. See exception.")
            print(e)
    else:
        print("Nothing to post")
    
    # Guardado de ajustes en archivo de configuración
    config = {"firstTime": False, "last_tweet": last_tweet.id, "index": index, "previous_film": previous_film}
    with open('config.json', 'w') as f:
        json.dump(config, f)

    # Esperar 15 minutos a la siguiente comprobación del feed RSS
    time.sleep(900)
