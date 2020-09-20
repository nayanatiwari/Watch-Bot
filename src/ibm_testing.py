from src.data_gathering import *
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import (
    CategoriesOptions, EntitiesOptions, Features, KeywordsOptions,
    SentimentOptions, EmotionOptions)

if __name__ != "__main__":
    raise ValueError()

with open("ibm_api.key", "r") as f:
    IBM_KEY = f.read().strip()

IBM_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c7bf3ab4-dcb6-488b-bd27-ea68c2525d7e"

NLP_Engine = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    iam_apikey=IBM_KEY,
    url=IBM_URL,
)



def sentiment_score(input_text): 
    # Input text can be sentence, paragraph or document
    response = NLP_Engine.analyze(text=input_text,
        features=Features(sentiment=SentimentOptions())
    ).get_result()
    # From the response extract score which is between -1 to 1
    res = response.get('sentiment').get('document').get('score')
    return res

def emotion(input_text): 
    # Input text can be sentence, paragraph or document
    response = NLP_Engine.analyze(text=input_text,
        features=Features(emotion=EmotionOptions())).get_result()
    # From the response extract score which is between -1 to 1
    res = response.get('sentiment').get('document').get('score')
    return res

def concepts(input_text): 
    pass

def ibm_request_loop(data):
    """
    make a request for each string in list data
    """
    out = []
    count = 0
    try:
        for i in data:
            if count % 20 == 0:
                print(count, end=" ")
            count += 1
            try:
                score = sentiment_score(i)
            except Exception as e:
                print("Exception:", e)
                score = None
            out.append(score)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    return out

print(emotion("Hello my name is ben and i'm excited to be here"))

# print("\n\npositive examples")

# p = load_json_data("pos_data")
# p = p[:2000]
# p_sent = ibm_request_loop(p)
# save_json_data(p_sent, "pos_data_sentiment")


# print("\n\nnegative examples")
# n = load_json_data("neg_data")
# n = n[:2000]
# n_sent = ibm_request_loop(n)
# save_json_data(n_sent, "neg_data_sentiment")