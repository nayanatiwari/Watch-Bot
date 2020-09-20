from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from sklearn.naive_bayes import MultinomialNB
import pandas as pd


def create_column_headers(data_set):
    column_headers = []
    doc_name = "Doc"
    for i in range(len(data_set)):
        column_headers.append(doc_name + str(i))
    return column_headers

"""
data_set : list of strings, each string being a document
returns: pandas matrix, words vectorized with tfidf
"""
def generate_tfidf_matrix(data_set, test=False, tfidf_vect=None):

    if not test:
        tfidf_vect = TfidfVectorizer(analyzer='word', stop_words='english')
        tfidf_wm = tfidf_vect.fit_transform(data_set)
        return tfidf_wm, tfidf_vect
    
    tfidf_wm = tfidf_vect.transform(data_set)

    return tfidf_wm, tfidf_vect


if __name__ == "__main__":
    pass
