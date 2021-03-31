#Importaciones: Tweepy para la API de Twitter y Feedparser para el feed RSS
import tweepy
import feedparser
import time
import os

from config import create_api


# TODO: Postear listas en otro hilo diferente
# FIXME: Actualmente si reinicias el programa siempre escribe de nuevo la última película, incluso si ya había sido escrita. Solución, volcar a fichero el ID del último tweet escrito asi como el índice y demás datos relevantes

api = create_api()

url = 'https://letterboxd.com/rbnmustdie/rss/'
last_tweet = api.get_status(1376990746084007941)
index = 1
previous_film = ""

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
        tweet_string = str(index) + ".- " + f['title']+'\n'+"    Link: " + str(f['link']).replace('(','',-1).replace(')','',-1).replace(',','',-1).replace('\'','',-1) +'\n'
        try:
            last_tweet = api.update_status(tweet_string, last_tweet.id)
            index += 1
            print("Posted tweet with id:", last_tweet.id)
        except Exception as e:
            print("Failed posting tweet. See exception.")
            print(e)

    time.sleep(60)
