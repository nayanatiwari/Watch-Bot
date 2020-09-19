from data_gathering import *
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import (
    CategoriesOptions, EntitiesOptions, Features, KeywordsOptions,
    SentimentOptions)

if __name__ != "__main__":
    raise ValueError()

"""
thanks to https://medium.com/@Intellica.AI/vader-ibm-watson-or-textblob-which-is-better-for-unsupervised-sentiment-analysis-db4143a39445
for the demo code
"""

with open("ibm_api.key", "r") as f:
    IBM_KEY = f.read().strip()

IBM_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/ce4dd669-c69f-4b3b-9fad-9d2b371ab2b5"

NLP_Engine = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    iam_apikey=IBM_KEY,
    url=IBM_URL,
)

COUNT = 0

def sentiment_score(input_text): 
    global COUNT
    if COUNT % 10 == 0:
        print(COUNT, end=" ", flush=True)
    COUNT += 1
    # Input text can be sentence, paragraph or document
    response = NLP_Engine.analyze(text=input_text,
        features=Features(sentiment=SentimentOptions())
    ).get_result()
    # From the response extract score which is between -1 to 1
    res = response.get('sentiment').get('document').get('score')
    return res


print("\n\npositive examples")
p = load_json_data("pos_data")
p_sent = [sentiment_score(i) for i in p]
save_json_data(p_sent, "pos_data_sentiment")

print("\n\nnegative examples")
n = load_json_data("neg_data")
n_sent = [sentiment_score(i) for i in n]
save_json_data(n_sent, "neg_data_sentiment")



