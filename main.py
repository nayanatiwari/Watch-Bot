import os
# pretty printing. just nice for visualizing big lists/dicts
from pprint import pprint
import numpy as np
import argparse

from data_processing import *
from scrape_reddit import *
from keras_model import *
from data_gathering import *

np.random.seed(0)
tf.random.set_seed(0)


parser = argparse.ArgumentParser()
parser.add_argument("--name",required=True,type=str,help="name to save this model under")
parser.add_argument("--minidata",action="store_true",default=False,help="use mini dataset (500 examples each)")
parser.add_argument("--epochs",type=int,default=200)
args = parser.parse_args()


### Load Data

# positive
if not os.path.exists("data/pos_data.json"):
    pos_examples = request_format_save(size=10000, pos=True)
else:
    pos_examples = load_json_data("pos_data")

# negative
if not os.path.exists("data/neg_data.json"):
    neg_examples = request_format_save(size=10000, pos=False)
else:
    neg_examples = load_json_data("neg_data")

print("Positive examples:", len(pos_examples), "Negative examples:", len(neg_examples))

# trim to 1000 words max, remove words with numbers
p = [i.split()[:1000] for i in pos_examples]
n = [i.split()[:1000] for i in neg_examples]
p = [[j for j in i if not re.match(r"[0-9]", j)] for i in p]
n = [[j for j in i if not re.match(r"[0-9]", j)] for i in n]
p = [" ".join(i) for i in p]
n = [" ".join(i) for i in n]

if args.minidata:
    p = p[:500]
    n = n[:500]

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


