import praw
import config

wiki = "www.wikipedia.org"
find = "!find"

def bot_login:
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Finder App for wiki and youtube")
    return r

def run_bot(r):
    for comment in r.subreddit("test").comments(limit=25):
        if  wiki in comment.body:
            print ("FOUND")

r = bot_login()
