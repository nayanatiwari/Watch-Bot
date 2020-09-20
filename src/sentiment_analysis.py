from src.data_gathering import *
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import (
    CategoriesOptions, EntitiesOptions, Features, KeywordsOptions,
    SentimentOptions, EmotionOptions)
import argparse

if __name__ != "__main__":
    raise ValueError()

"""
thanks to https://medium.com/@Intellica.AI/vader-ibm-watson-or-textblob-which-is-better-for-unsupervised-sentiment-analysis-db4143a39445
for the demo code
"""

with open("ibm_api.key", "r") as f:
    lines = f.readlines()
    IBM_KEY, IBM_URL = lines[0].strip(), lines[1].strip()
    print(IBM_KEY)
    print(IBM_URL)


NLP_Engine = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    iam_apikey=IBM_KEY,
    url=IBM_URL,
)


def sentiment_score(input_text):
    # Input text can be sentence, paragraph or document
    response = NLP_Engine.analyze(text=input_text,
        features=Features(sentiment=SentimentOptions(), emotion=EmotionOptions())
    ).get_result()
    # From the response extract score which is between -1 to 1
    sentiment = response.get('sentiment').get('document').get('score')
    emotion = response.get('emotion').get('document')
    return sentiment, emotion


def ibm_request_loop(data):
    """
    make a request for each string in list data
    """
    sentims = []
    emotions = []
    count = 0
    try:
        for i in data:
            if count % 20 == 0:
                print(count, end=" ", flush=True)
            count += 1
            try:
                sent, emot = sentiment_score(i)
            except Exception as e:
                print("Exception:", e)
                sent, emot = 0.0, {"sadness":0.0, "joy":0.0, "fear":0.0, "disgust":0.0, "anger":0.0}
            sentims.append(sent)
            emotions.append(emot)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    return sentims, emotions


parser = argparse.ArgumentParser()
parser.add_argument("--pos",action="store_true",default=False)
args = parser.parse_args()

if args.pos:
    print("\n\npositive examples")
    p = load_json_data("pos_data")
    p = p[2000:]
    p_sent = ibm_request_loop(p)
    save_json_data(p_sent, "pos_data_sentiment")

else:
    print("\n\nnegative examples")
    n = load_json_data("neg_data")
    n = n[2000:]
    n_sent = ibm_request_loop(n)
    save_json_data(n_sent, "neg_data_sentiment")


