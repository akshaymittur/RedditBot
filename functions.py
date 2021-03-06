import praw
import config
import time
import os
import requests
from bs4 import BeautifulSoup
import re
import wikipediaapi

wiki = "!wiki"
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
        wiki_func(wiki, comment, comments_replied_to, r)

        #Finding Comments with joke, and replying with a joke
        joke_func(joke, comment, comments_replied_to, r)

        #Finding Comments with kanye, and replying with a kanye quote
        kanye_func(kanye, comment, comments_replied_to, r)

        #Finding Comments with find, and replying with a youtube link
        find_func(find, comment, comments_replied_to, r)

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

#Finding Comments with wiki, and replying with wikipedia summary
def wiki_func(wiki, comment, comments_replied_to, r):
    if wiki in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
        print ("FOUND WIKI")
        reply = "You Requested a Wikipedia Summary, Here it is! \n\n"

        search = re.search(r'(?<=!wiki)[^.]*',comment.body).group(0)
        search = search[1:]

        wiki_lang = wikipediaapi.Wikipedia('en')
        wiki_page = wiki_lang.page(search)

        if not wiki_page.exists():
            comment.reply("Sorry, Page Does Not Exist!")
        else:
            if "may refer to" in wiki_page.summary:
                comment.reply("Be More Specific Please!")
            else:
                comment.reply(reply + ">" + wiki_page.summary)

        comments_replied_to.append(comment.id)

        with open("comments_replied_to.txt", "a") as f:
            f.write(comment.id + "\n")

#Finding Comments with joke, and replying with a joke
def joke_func(joke, comment, comments_replied_to, r):
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
def kanye_func(kanye, comment, comments_replied_to, r):
    if kanye in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
        print ("FOUND KANYE")
        reply = "You Requested a Kanye West Quote, Here it is! \n\n"
        quote = requests.get("https://api.kanye.rest/").json()["quote"]

        comment.reply(reply + ">" + quote)

        comments_replied_to.append(comment.id)

        with open("comments_replied_to.txt", "a") as f:
            f.write(comment.id + "\n")

#Finding Comments with find, and replying with a youtube link
def find_func(find, comment, comments_replied_to, r):
    if find in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
        print ("FOUND FIND")
        reply = "You Requested a YouTube Link, Here it is! \n\n"
        url = "https://www.youtube.com/results?search_query="
        search = re.search(r'(?<=!find)[^.]*',comment.body).group(0)

        if len(search):
            search = search.replace(" ", "+")
            url += search[1:]

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            div = [ d for d in soup.find_all("div") if d.has_attr("class") and "yt-lockup-dismissable" in d["class"] ]
            a = [ x for x in div[0].find_all("a") if x.has_attr("title") ]

            comment.reply(reply + ">" +"https://www.youtube.com" + a[0]["href"])

        else:
            comment.reply("Sorry! Not Found")
            
        comments_replied_to.append(comment.id)

        with open("comments_replied_to.txt", "a") as f:
            f.write(comment.id + "\n")