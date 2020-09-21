import reddit_interface
from user import User

def add_users_to_database(users):
    fp = open("users_database.txt", "w")
    #set contact_person to username of test account. Do not actually send messages to
    #reddit users for testing. For now, send messages to self.
    contact_person = 'Watch-Bot'
    for user in users:
        fp.write("{0},{1},{2}\n".format(user, [contact_person], True))
    fp.close()

def add_data_to_users(subreddit_list, users):
    for i in subreddit_list:
        data = reddit_interface.get_post_authors(i, 5)
        for i in data:
            if i['author'] != "[deleted]" and i['author'] not in users:
                users.append(i['author'])

def get_users():
    users = []
    data = reddit_interface.get_post_authors("SuicideWatch", 55)
    for i in data:
        if i['author'] != "[deleted]":
            users.append(i['author'])
    subreddit_list = ["calpoly", "tifu", "todayileraned", "xxFitness", "relationshipadvice", "legaladvice",
        "lifeofnorman", "talesfromtechsupport", "britishproblems", "writingprompts", "outoftheloop"]
    add_data_to_users(subreddit_list, users)
    return users
    

def main():
    users = get_users()
    add_users_to_database(users)

if __name__=="__main__":
    main()