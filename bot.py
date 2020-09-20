import praw
import logging
from user import User
            
def reply_to_enrollment_message(message, users):
    enrollment_reply_message = "Thank you for reaching out to Watch-Bot! If you are having suicidal thoughts please\
 call this crisis line:  1-800-273-8255 or [chat](http://chat.suicidepreventionlifeline.org/GetHelp/LifelineChat.aspx)\
 via [Suicide Prevention Resource Center]( http://www.sprc.org/).\n\nIf you are interested in our service\
 please reply with the reddit username of someone who can be contacted if you post something determined to have suicidal\
 sentiment.\n\nFor your message, type Contact: [reddit username],[reddit username],[reddit username] with no\
 spaces between the commas!\n\n You can opt-out at any time by sending us a message with LEAVE in it."
    new_user = User(message.author)
    users.update({new_user.redditor:new_user})
    message.mark_read()
    message.reply(enrollment_reply_message)

def check_for_enrollment_message(message, users):
    subject_line_options = ["enroll in watch-bot", "enroll in watchbot", "enroll"]
    subject = message.subject.lower().strip()
    valid_subject = False
    for option in subject_line_options:
        if option in subject:
            valid_subject = True
    if message.subreddit is None and valid_subject and message.author not in users:
            return True
    return False

def iterate_contact_info_message(message, users, reddit):
    message_list = message.body.split()
    for index in range(0, len(message_list) - 1):
        word = message_list[index]
        if word.lower() == "contact:":
            reply_to_contact_info_message(message, users, message_list[index+1], reddit)
    else:
        default_reply(message, users)

def default_reply(message, users):
    if message.author in users and users[message.author].finished_enrolling:
        enrolled_status_message = "You are already enrolled in the Watch-Bot service. There\
are no additional steps at this time. Thank you!"
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
        users[message.author].contacts = contacts
        users[message.author].finished_enrolling = True
        message.mark_read()
        contact_info_reply_message = "Thank you for submitting your contact information! If a suicidal post \
is detected the users " + print_contacts(contacts) + " will be contacted via private message. You are officially \
enrolled in Watch-Bot. We look forward to helping you on your mental health journey :)"
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
    if message.author in users and "contact: " in message.body.lower():
        return True
    return False

def check_for_leave_message(message, users):
    if "leave" in message.body.lower() and message.author in users:
        return True
    return False

def reply_to_leave_message(message, users):
    users.pop(message.author)
    message.mark_read()
    leave_reply_message = "You have successfully opted out of the Watch-Bot service, \
If you are having any suicidal thoughts please call this crisis line:  1-800-273-8255 \
or [chat](http://chat.suicidepreventionlifeline.org/GetHelp/LifelineChat.aspx) \
via [Suicide Prevention Resource Center]( http://www.sprc.org/).\n\nYou can opt-in again \
at anytime. Thank you and we wish you the best!"
    message.reply(leave_reply_message)

def notify_contacts(redditor, users, reddit):
    contacts = users[redditor].contacts
    for contact in contacts:
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

def main():
    reddit = praw.Reddit('Watch-Bot')
    users = {}
    while 1:
        check_unread_messages(reddit, users)

if __name__ == "__main__":
    main()
