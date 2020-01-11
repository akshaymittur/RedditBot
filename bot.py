import praw
import config
import time

wiki = "wikipedia.org"
find = "!find"

def bot_login():
    print("Logging In")
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Finder App for wiki and youtube")
    print("Logged In")
    return r

def run_bot(r):
    print("Obtaining Comments")
    for comment in r.subreddit("test").comments(limit=25):
        if wiki in comment.body:
            print ("FOUND")
            comment.reply("Found!")
            print("Replied to Comment " + comment.id)
    print("Sleeping for 10 Seconds")
    #Sleeping for 10 Seconds
    time.sleep(10)

r = bot_login()
run_bot(r)
