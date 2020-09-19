from data_gathering import load_json_data
import re

def get_data_from_directory():

    # positive
    pos_examples = load_json_data("pos_data")
    neg_examples = load_json_data("neg_data")
    maxWords = 1000

    # trim to data maxWords, remove words with numbers
    p = [i.split()[:maxWords] for i in pos_examples]
    n = [i.split()[:maxWords] for i in neg_examples]
    p = [[j for j in i if not re.match(r"[0-9]", j)] for i in p]
    n = [[j for j in i if not re.match(r"[0-9]", j)] for i in n]
    p = [" ".join(i) for i in p]
    n = [" ".join(i) for i in n]

    return p, n

if __name__ == "__main__":
    get_data_from_directory()
