import praw

class User:
    def __init__(self, user, message_name):
        self.redditor = user
        self.contacts = []
        self.finished_enrolling = False
        self.previous_messages = [message_name]
    
    def __str__(self):
        return ("User: {0}\tContacts: {1}\tFinished Enrolling?: {2}\tmessage ids: {3}".format(
            self.redditor.name, self.contacts, self.finished_enrolling, self.previous_messages))