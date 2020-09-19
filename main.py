import os
# pretty printing. just nice for visualizing big lists/dicts
from pprint import pprint
import numpy as np
import argparse

from data_processing import *
from scrape_reddit import *
from keras_model import *
from data_gathering import *

# np.random.seed(0)
# tf.random.set_seed(0)


parser = argparse.ArgumentParser()
parser.add_argument("--name",required=True,type=str,help="name to save this model under")
parser.add_argument("--datasize",type=int,default=10_000,help="numbers of examples for each class to use")
parser.add_argument("--epochs",type=int,default=200)
parser.add_argument("--batchsize",type=int,default=128)
parser.add_argument("--test",action="store_true",default=False,help="only test model")
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


p = pos_examples[:args.datasize]
n = neg_examples[:args.datasize]

# trim to 1000 words max, remove words with numbers
p = [i.split()[:1000] for i in p]
n = [i.split()[:1000] for i in n]
p = [[j for j in i if not re.match(r"[0-9]", j)] for i in p]
n = [[j for j in i if not re.match(r"[0-9]", j)] for i in n]
p = [" ".join(i) for i in p]
n = [" ".join(i) for i in n]

# combine and shuffle
data = np.array(p + n)
labels = np.array([1 for i in p] + [0 for i in n])

indices = np.arange(len(data))
np.random.shuffle(indices)
slabels = labels[indices]
sdata = data[indices]

# calculate number of words
d = {}
for i in p+n:
    for j in i.split():
        d[j] = 0
print(len(d), "unique words")

### Run Model

model = OurModel(sdata, slabels, args=args)
if not args.test:
    model.train()
model.test(name=args.name)

