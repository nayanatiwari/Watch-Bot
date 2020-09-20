import praw
import logging
from src import reddit_interface
from src.predictor import get_prediction
from src.user import User
PREDICTION_MODEL = "naivebayes"

def upload_users_database(users):
    fp = open("users_database.txt", "r")
    lines = fp.readlines()
    fp.close()
    for line in lines:
        line_list = line.split(",")
        new_user = User(line_list[0])
        new_user.contacts = line_list[1].strip('][').split(', ') 
        if (line_list[2].strip()) == "True":
            new_user.finished_enrolling = True
        else:
            new_user.finished_enrolling = False
        users[new_user.redditor] = new_user

def update_users_database(user):
    fp = open("users_database.txt", "a")
    fp.write("{0},{1},{2}\n".format(user.redditor, 
        user.contacts, user.finished_enrolling))
    fp.close()

def update_contact_info_in_database(user):
    fp = open("users_database.txt", "r")
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        line_list = lines[i].split(",")
        if user.redditor == line_list[0]:
            lines[i] = "{0},{1},{2}\n".format(user.redditor, 
        user.contacts, user.finished_enrolling)
    fp = open("users_database.txt", "w")
    for line in lines:
        fp.write(line)
    fp.close()

def delete_user_from_database(redditor):
    fp = open("users_database.txt", "r")
    lines = fp.readlines()
    write_lines = []
    for i in range(len(lines)):
        line_list = lines[i].split(",")
        if redditor != line_list[0]:
            write_lines.append(lines[i])
    fp = open("users_database.txt", "w")
    for line in write_lines:
        fp.write(line)
    fp.close()
            
def reply_to_enrollment_message(message, users):
    enrollment_reply_message = "Thank you for reaching out to Watch-Bot! If you are having suicidal thoughts please\
 call this crisis line:  1-800-273-8255 or [chat](http://chat.suicidepreventionlifeline.org/GetHelp/LifelineChat.aspx)\
 via [Suicide Prevention Resource Center]( http://www.sprc.org/).\n\nIf you are interested in our service\
 please reply with the reddit username of someone who can be contacted if you post something determined to have suicidal\
 sentiment.\n\nFor your message, type Contact: [reddit username],[reddit username],[reddit username] with no\
 spaces between the commas!\n\n You can opt-out at any time by sending us a message with LEAVE in it."
    new_user = User(str(message.author))
    users.update({new_user.redditor:new_user})
    update_users_database(new_user)
    message.mark_read()
    message.reply(enrollment_reply_message)

def check_for_enrollment_message(message, users):
    subject_line_options = ["enroll in watch-bot", "enroll in watchbot", "enroll"]
    subject = message.subject.lower().strip()
    valid_subject = False
    for option in subject_line_options:
        if option in subject:
            valid_subject = True
    if message.subreddit is None and valid_subject and str(message.author) not in users.keys():
        return True
    return False

def iterate_contact_info_message(message, users, reddit):
    message_list = message.body.split()
    replied = False
    for index in range(0, len(message_list) - 1):
        word = message_list[index]
        if word.lower() == "contact:" and not replied:
            reply_to_contact_info_message(message, users, message_list[index+1], reddit)
            replied = True
    if not replied:
        default_reply(message, users)

def default_reply(message, users):
    redditor = str(message.author)
    if redditor in users and users[redditor].finished_enrolling:
        enrolled_status_message = "You are already enrolled in the Watch-Bot service. There \
are no additional steps at this time. Opt-out by messaging us \"LEAVE\". Thank you!"
    else:
        enrolled_status_message = "You have not completed your enrollment. If you are trying to add contacts \
send a message only containing the following with the number of reddit contacts you prefer \
(no spaces between usernames please!)- Contact: [reddit username],[reddit username],[reddit username]"
    default_reply_message = "Hmmm I don't understand what you said. " + enrolled_status_message
    message.mark_read()
    message.reply(default_reply_message)


def reply_to_contact_info_message(message, users, contacts, reddit):
    contacts = contacts.split(",")
    if not validate_contacts(reddit, contacts):
        message.mark_read()
        invalid_contact_info_reply_message = "The contacts you provided were not all valid \
redditors. Please verify their usernames and submit the \"Contact: [reddit username],[reddit username]\" \
message again."
        message.reply(invalid_contact_info_reply_message)
    else:
        user = users[str(message.author)]
        user.contacts = contacts
        user.finished_enrolling = True
        update_contact_info_in_database(user)
        message.mark_read()
        contact_info_reply_message = "Thank you for submitting your contact information! If a suicidal post \
is detected the users " + print_contacts(contacts) + " will be contacted via private message. You are officially \
enrolled in Watch-Bot. Opt-out at anytime by messaging us \"LEAVE\". We look forward to helping you on your mental health journey :)"
        message.reply(contact_info_reply_message)

def print_contacts(contacts):
    string = ''
    for i in contacts:
        string += i
        if i != len(contacts) - 1:
            string += ", "
    return string

def validate_contacts(reddit, contacts):
    for i in range(0, len(contacts)):
        contact = contacts[i]
        if len(contact) > 2 and "u/" == contact[:2]:
            contacts[i] = contact[2:]
        redditor = reddit.redditor(contacts[i])
        #invalid contact
        try:
            a = redditor.id
        except:
            return False
    return True

def check_for_contact_info_message(message, users):
    if str(message.author) in users and "contact: " in message.body.lower():
        return True
    return False

def check_for_leave_message(message, users):
    if "leave" in message.body.lower() and str(message.author) in users:
        return True
    return False

def reply_to_leave_message(message, users):
    users.pop(str(message.author))
    delete_user_from_database(str(message.author))
    message.mark_read()
    leave_reply_message = "You have successfully opted out of the Watch-Bot service, \
If you are having any suicidal thoughts please call this crisis line:  1-800-273-8255 \
or [chat](http://chat.suicidepreventionlifeline.org/GetHelp/LifelineChat.aspx) \
via [Suicide Prevention Resource Center]( http://www.sprc.org/).\n\nYou can opt-in again \
at anytime. Thank you and we wish you the best!"
    message.reply(leave_reply_message)

def notify_contacts(redditor, users, reddit):
    if not users[redditor].notified_contacts:
        contacts = users[redditor].contacts
        for contact in contacts:
            contact = contact.strip('\'')
            users[redditor].notified_contacts = True
            message = create_notification_message(contact, redditor)
            reddit.redditor(contact).message('WARNING: {0} Suicidal Post Flag'.format(redditor), message)

def create_notification_message(contact, redditor):
    return "Hi {0}, this is Watch-Bot, a service your friend {1} to monitor their posts \
for suicidal sentiment. We have flagged a recent post of theirs. Please check in with \
them and any of their close friends and family. If you are unsure what to do, please refer to \
[Suicide Prevention Resource Center]( http://www.sprc.org/). Thank you for your help".format(contact, redditor)

def start_logging():
    #from PRAW documentation - not original content
    #used for debugging
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    for logger_name in ("praw", "prawcore"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

def check_unread_messages(reddit, users):
    for message in reddit.inbox.unread():
        if check_for_enrollment_message(message, users):
            reply_to_enrollment_message(message, users)
        elif check_for_contact_info_message(message, users):
            iterate_contact_info_message(message, users, reddit)
        elif check_for_leave_message(message, users):
            reply_to_leave_message(message, users)
        else:
            default_reply(message, users)

def check_user_posts(reddit, users):
    for user in users:
        try:
            post_data = reddit_interface.get_user_posts(user)
        except ValueError as e:
            post_data = []

        if post_data == []:
            continue

        # combine posts into one long string to treat as single doc
        post_data_one_doc = " ".join(post_data)
        prediction = get_prediction(PREDICTION_MODEL, documents=[post_data_one_doc]) 
        
        if prediction[0] == 1:
            notify_contacts(users[user].redditor, users, reddit) 
    
def main():
    reddit = praw.Reddit('Watch-Bot')
    users = {}
    upload_users_database(users)
    while 1:
        check_unread_messages(reddit, users)
        check_user_posts(reddit, users)
        print("end of first run")

if __name__ == "__main__":
    main()
