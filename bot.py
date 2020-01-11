import praw
import config
import time

wiki = "wikipedia.org"
find = "!find"
comments_replied_to = []

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
        if wiki in comment.body and comment.id not in comments_replied_to:
            print ("FOUND")
            comment.reply("Found!")
            print("Replied to Comment " + comment.id)

            comments_replied_to.append(comment.id)

    print("Sleeping for 5 Seconds")
    #Sleeping for 10 Seconds
    time.sleep(5)

r = bot_login()
run_bot(r)
