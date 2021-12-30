import feedparser
import time
import json
import emoji
from config import create_api

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
            description = e.description

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
                    'published': published,
                    'description': description
                }
                films_list.append(film)

        return films_list, lists
    except Exception as e:
        print('The scraping job failed. See exception: ')
        print(e)

firstTime = True

# Edit this with your letterboxd feed
url = 'https://letterboxd.com/rbnmustdie/rss/'

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    firstTime = config["firstTime"]
except Exception as e:
    print (e)

if firstTime:
    films_raw_data, lists_raw_data = letterboxd_rss()
    last_film = films_raw_data[1]
    next_to_last_film = films_raw_data[2]
    config = {"firstTime": False,
    # Edit this with your first tweet ID
    "last_tweet": 1476657518759890949,
    "index": 1,
    "next_to_last_film": next_to_last_film, 
    "last_film": last_film}
    with open('config.json', 'w') as f:
        json.dump(config, f)

api = create_api()

last_tweet = api.get_status(config["last_tweet"])
next_to_last_tweet = api.get_status(config["next_to_last_tweet"])
index = config["index"]
last_film = config["last_film"]
next_to_last_film = config["next_to_last_film"]

while True:
    print('Starting scraping')

    films_raw_data, lists_raw_data = letterboxd_rss()

    tweet_string = ""
    scrapped_film = films_raw_data[0]

    if scrapped_film['link'] != last_film['link'] and scrapped_film['link'] != next_to_last_film['link']:
        next_to_last_film = last_film
        last_film = scrapped_film
        emoji_star = emoji.emojize(":star:")
        star = u"\u2605"
        tweet_string = str(index) + ".- " + str(scrapped_film['title']).replace(star, emoji_star, -1) +'\n' + str(scrapped_film['link']).replace('(','',-1).replace(')','',-1).replace(',','',-1).replace('\'','',-1) +'\n'
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
    
    config = {"firstTime": False,
    "last_tweet": last_tweet.id,
    "index": index,
    "next_to_last_film": next_to_last_film, 
    "last_film": last_film}
    with open('config.json', 'w') as f:
        json.dump(config, f)

    # Wait 15 minutes between checks
    time.sleep(900)
