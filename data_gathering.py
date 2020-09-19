import json
import os
import time

from data_processing import *

def save_json_data(data, filename):
    with open("data/"+filename+".json", "w") as f:
        json.dump(data, f, indent=2)


def load_json_data(filename):
    with open("data/"+filename+".json", "r") as f:
        data = json.load(f)
    return data


def request_loop(size, subreddits):
    """
    """
    sub_i = 0
    data = []
    before = None
    while len(data) < size:
        # make request
        print("requesting from", subreddits[sub_i] + ".", len(data), "so far")
        try:
            batch = pushshift_request(subreddit=subreddits[sub_i], before=before)
        except Exception as e:
            print("Exception:", e)
            print("Waiting 10 seconds...")
            time.sleep(10)
            continue
        # update timestamp
        utcs = [i["created_utc"] for i in batch]
        before = min(utcs)
        # format
        formatted = format_comments(batch)
        data.extend(formatted)
        # next subreddit
        sub_i = (sub_i + 1) % len(subreddits)
        # slight pause, to be nice to pushshift
        time.sleep(0.1)
    return data

def request_format_save(size, pos=True):
    """
    request a new set of data ('size' examples of each), format it, and save it
    """
    p_subs = ["SuicideWatch"]
    n_subs = ["CasualConversation", "NonZeroDay", "ShowerThoughts", "LifeProTips", 
        "books", "stories"]
    if pos:
        data = request_loop(size, p_subs)
        save_json_data(data, "pos_data")
    else:
        data = request_loop(size, n_subs)
        save_json_data(data, "neg_data")
    return data


