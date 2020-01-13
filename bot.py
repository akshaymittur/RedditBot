import praw
import config
import time
import os
import requests

wiki = "wikipedia.org"
find = "!find"
joke = "!joke"

def bot_login():
    print("Logging In")
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Finder App for wiki and youtube")
    print("Logged In")
    return r

def run_bot(r, comments_replied_to):
    print("Obtaining Comments")

    for comment in r.subreddit("test").comments(limit=25):
        if wiki in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
            print ("FOUND WIKI")
            comment.reply("Found!")

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

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
