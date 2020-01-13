import praw
import config
import time
import os
import requests
from bs4 import BeautifulSoup
import re

wiki = "wikipedia.org"
find = "!find"
joke = "!joke"
kanye = "!kanye"

#For Logging In
def bot_login():
    print("Logging In")
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Finder App for wiki and youtube")
    print("Logged In")
    return r

#For Running Bot
def run_bot(r, comments_replied_to):
    print("Obtaining Comments")

    #Finding Comments
    for comment in r.subreddit("test").comments(limit=25):
        #Finding Comments with wiki, and replying with wikipedia summary
        if wiki in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
            print ("FOUND WIKI")
            comment.reply("Found!")

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

        #Finding Comments with joke, and replying with a joke
        if joke in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
            print ("FOUND JOKE")
            reply = "You Requested a Joke, Here it is! \n\n"
            joke_type = "twopart"
            while joke_type == "twopart":
                random_joke = requests.get("https://sv443.net/jokeapi/category/Any").json()
                if joke_type == random_joke["type"]:
                    continue
                else :
                    punchline = random_joke["joke"]
                    joke_type = random_joke["type"]

            comment.reply(reply + ">" + punchline)

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

        #Finding Comments with kanye, and replying with a kanye quote
        if kanye in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
            print ("FOUND KANYE")
            reply = "You Requested a Kanye West Quote, Here it is! \n\n"
            quote = requests.get("https://api.kanye.rest/").json()["quote"]

            comment.reply(reply + ">" + quote)

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

        #Finding Comments with find, and replying with a youtube link
        if find in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
            print ("FOUND FIND")
            url = "https://www.youtube.com/results?search_query="
            search = re.search(r'(?<=!find)[^.]*',comment.body).group(0)

            search = search.replace(" ", "+")
            url += search[1:]
            print(url)
            #comment.reply()

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print("Sleeping for 5 Seconds")
    #Sleeping for 10 Seconds
    time.sleep(5)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))
    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()

while True:
    run_bot(r, comments_replied_to)
