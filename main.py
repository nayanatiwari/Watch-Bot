import json
import os
# pretty printing. just nice for visualizing big lists/dicts
from pprint import pprint
import numpy as np
import argparse

from data_processing import *
from scrape_reddit import *
from keras_model import *

# np.random.seed(0)
# tf.random.set_seed(0)

def save_data(data, filename):
    with open("data/"+filename+".json", "w") as f:
        json.dump(data, f, indent=2)


def load_data(filename):
    with open("data/"+filename+".json", "r") as f:
        comments = json.load(f)
    return comments


parser = argparse.ArgumentParser()
parser.add_argument("--name",required=True,type=str,help="name to save this model under")
parser.add_argument("--epochs",type=int,default=200)
args = parser.parse_args()

### Load Data

if not os.path.exists("data/neg_data.json"):
    pos_comments = get_comments(subreddit="SuicideWatch")
    save_data(pos_comments, "pos_data")
    neg_comments = get_comments(subreddit="CasualConversation")
    save_data(neg_comments, "neg_data")
else:
    pos_comments = load_data("pos_data")
    neg_comments = load_data("neg_data")
print("Positive examples:", len(pos_comments), "Negative examples:", len(neg_comments))

p = format_comments(pos_comments)
n = format_comments(neg_comments)

# combine and shuffle
data = np.array(p + n)
labels = np.array([1 for i in p] + [0 for i in n])

indices = np.arange(len(data))
np.random.shuffle(indices)
slabels = labels[indices]
sdata = data[indices]

### Run Model

model = OurModel(sdata, slabels, args=args)
model.run()


