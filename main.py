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
    p = request_format_save(size=10000, pos=True)
else:
    p = load_json_data("pos_data")

# negative
if not os.path.exists("data/neg_data.json"):
    n = request_format_save(size=10000, pos=False)
else:
    n = load_json_data("neg_data")

print("Positive examples:", len(p), "Negative examples:", len(n))


# trim to 1000 words max, remove words with numbers
p = [i.split()[:1000] for i in p]
n = [i.split()[:1000] for i in n]
p = [[j for j in i if not re.match(r"[0-9]", j)] for i in p]
n = [[j for j in i if not re.match(r"[0-9]", j)] for i in n]
p = [" ".join(i) for i in p]
n = [" ".join(i) for i in n]

p_rest = p[args.datasize:]
n_rest = n[args.datasize:]
p = p[:args.datasize]
n = n[:args.datasize]

# combine and shuffle
data = np.array(p + n)
labels = np.array([1 for i in p] + [0 for i in n])

data_rest = np.array(p_rest + n_rest)
labels_rest = np.array([1 for i in p_rest] + [0 for i in n_rest])

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

rest_len = len(data_rest)
data_rest = model.make_hash_words(data_rest)


def run_tests(model):
    model.test(model.x, model.y, name="training set")
    model.test(model.valx, model.valy, name="validation set")
    if rest_len > 0:
        model.test(data_rest, labels_rest, "rest set (" + str(rest_len) + " unseen examples)")
    else:
        print("No rest set")

print("\n--- Final Model ---")
modelname = "models/" + args.name + "_final.hdf5"
model.model = keras.models.load_model(modelname)
run_tests(model)

print("\n--- Best Validation Loss Model ---")
modelname = "models/" + args.name + "_best_val_loss.hdf5"
model.model = keras.models.load_model(modelname)
run_tests(model)

