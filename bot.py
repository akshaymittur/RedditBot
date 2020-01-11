import praw
import config

def bot_login:
    r = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Finder App for wiki and youtube")
    return r

def run_bot(r):


r = bot_login()
