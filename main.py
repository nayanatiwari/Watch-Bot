from pprint import pprint # pretty printing. just nice for visualizing big lists/dicts
import json

from scrape_reddit import *
from data_processing import *

def save_data(data, filename="test_data"):
    with open(filename+".json", "w") as f:
        json.dump(data, f, indent=2)


def get_test_data(filename="test_data"):
    with open("test_data.json", "r") as f:
        comments = json.load(f)
    return comments

def main():
    # comments = get_comments(subreddit="SuicideWatch")
    # save_data(comments)
    comments = get_test_data()
    get_comments(before=min([i["created_utc"] for i in comments]), subreddit="SuicideWatch")

    test = format_comments(comments)
    print(test)


if __name__ == "__main__":
    main()