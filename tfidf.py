from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from sklearn.naive_bayes import MultinomialNB
import pandas as pd


def create_column_headers(data_set):
    column_headers = []
    doc_name = "Doc"
    for i in len(data_set):
        column_headers.append(doc_name += str(i))
    return column_headers

"""
data_set : list of strings, each string being a document
returns: pandas matrix, words vectorized with tfidf
"""
def generate_tfidf_matrix(data_set):

    column_headers = create_column_headers(data_set)
    tfidf_wm = tfidfvectorizer.fit_transform(train)
    tfidf_tokens = tfidfvectorizer.get_feature_names()

    # this datafram for printing
    df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(), index = column_headers,
                            columns = tfidf_tokens)

    return tfidf_wm


if __name__ == "__main__":

