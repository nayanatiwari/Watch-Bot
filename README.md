# Watch-Bot

HackMIT 2020 Project

Reddit bot service that users can opt-in to that montiors user's posts for suicidal sentiment (using Machine Learning, Naive Bayes Classifier, IBM Watson). If a suicidal post is detected, the user-defined emergency contacts are notified. This is not for currently high-risk people - suicide prevention lifelines and resources are included throughout the program. Rather, we imagine those who have recently recovered or completed therapy would use this service to keep a continuous check on their mental health.

Check out [u/Watch-Bot](https://www.reddit.com/user/Watch-Bot)

[Ben Lucero](https://www.github.com/benicero) (Pitzer College), [Ryan Hunter](https://www.github.com/0sesame), [Nayana Tiwari](https://www.github.com/nayanatiwari), [Julian Rice](https://www.github.com/jrice15) (rest from Cal Poly San Luis Obispo)

## Dependancies
  The most recent releases of sklearn, matplotlib, keras, praw, and seaborn are required to run the Watch-Bot

## Models and Classification

The Watch-Bot collects user posts and combines them as one document. Then, it vectorizes the data and attempts to classify the posts as either 1: high-risk for 
suicide or 0: not a high-risk for suicide.

The Watch-Bot currently implements a variety of classifying models to do this classification, and, in production, currently uses the highest preforming model: 
Multinomial Naive Bayesian classification.

### Generating models
  `python3 generate_model.py` will walk you through generating an available non-nueral-net model. It will also output the models results against test data.
  
## Running Watch-Bot
To run Watch-Bot, you'll need reddit api credentials in a file named `praw.ini` in your the base directory of this repository. For demos and tests, please refer to our [slide deck](https://docs.google.com/presentation/d/1M1LxWT-19T4gwqKPujl4ypH3b4fAiF-1Zl8KJHEsuTc/edit). The bot can be run with `python3 bot.py` Test user database can be configured with `python3 test_cases.py` to create a user_database.txt. This file should exist in the top directory for a maintained database between each instance.


# Structural Future Changes
The different python files for the models are an un-needed leftover of hacking this together. They could easily be abstracted to a single object initialized 
based on desired model. The neural-net models could also be attached to the same interface.
