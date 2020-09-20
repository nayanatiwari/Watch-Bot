# Watch-Bot

HackMIT 2020 Project

Reddit bot service that users can opt-in to that montiors user's posts for suicidal sentiment (using Machine Learning, Naive Bayes Classifier, IBM Watson). If a suicidal post is detected, the user-defined emergency contacts are notified. This is not for currently high-risk people - suicide prevention lifelines and resources are included throughout the program. Rather, we imagine those who have recently recovered or completed therapy would use this service to keep a continuous check on their mental health.

Check out [u/Watch-Bot](https://www.reddit.com/user/Watch-Bot)

[Ben Lucero](https://www.github.com/benicero) (Pitzer College), [Ryan Hunter](https://www.github.com/0sesame), [Nayana Tiwari](https://www.github.com/nayanatiwari), [Julian Rice](https://www.github.com/jrice15) (rest from Cal Poly San Luis Obispo)

## Dependancies
  The most recent releases of sklearn, matplotlib, keras, and seaborn are required to run the Watch-Bot

## Models and Classification

The Watch-Bot collects user posts and combines them as one document. Then, it vectorizes the data and attempts to classify the posts as either 1: high-risk for 
suicide or 0: not a high-risk for suicide.

The Watch-Bot currently implements a variety of classifying models to do this classification, and, in production, currently uses the highest preforming model: 
Multinomial Naive Bayesian classification.

### Generating models
  `python3 generate_model.py` will walk you through generating an available non-nueral-net model. It will also output the models results against test data.
