import json
import os
# pretty printing. just nice for visualizing big lists/dicts
from pprint import pprint

from data_processing import *
from scrape_reddit import *


def save_data(data, filename="test_data"):
    with open(filename+".json", "w") as f:
        json.dump(data, f, indent=2)


def get_test_data(filename):
    with open(filename+".json", "r") as f:
        comments = json.load(f)
    return comments

def main():
    if not os.path.exists("pos_data.json"):
        pos_comments = get_comments(subreddit="SuicideWatch")
        neg_comments = get_comments(subreddit="CasualConversation")
    else:
        pos_comments = get_test_data("pos_data")
        neg_comments = get_test_data("neg_data")
    print("Positive examples:", len(pos_comments), "Negative examples:", len(neg_comments))

    p = format_comments(pos_comments)
    n = format_comments(neg_comments)



if __name__ == "__main__":
    main()
