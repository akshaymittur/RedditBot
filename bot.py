import functions as func

r = func.bot_login()
comments_replied_to = func.get_saved_comments()

while True:
    func.run_bot(r, comments_replied_to)
