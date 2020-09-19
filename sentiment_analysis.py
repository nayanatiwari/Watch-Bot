from data_gathering import *
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import (
    CategoriesOptions, EntitiesOptions, Features, KeywordsOptions,
    SentimentOptions)

"""
thanks to https://medium.com/@Intellica.AI/vader-ibm-watson-or-textblob-which-is-better-for-unsupervised-sentiment-analysis-db4143a39445
for the demo code
"""

with open("ibm_api.key", "r") as f:
    IBM_KEY = f.read().strip()

IBM_URL = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/ce4dd669-c69f-4b3b-9fad-9d2b371ab2b5"

NLP_Engine = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
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



test1 = 'hello i am a happy bub'
test2 = 'hello i am a sad bub'

test3 = 'there is sun outside today'
test4 = "there isn't sun outside today"

test5 = "i wish i didn't want to die"
test6 = "i am going to die"

print(sentiment_score(test5))
print(sentiment_score(test6))
