from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
import pandas as pd

countvectorizer = CountVectorizer(analyzer='word', stop_words='english')
tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')

with open('train_data.txt', 'r') as f:
    train = f.readlines()

with open('test_data.txt', 'r') as f:
    test = f.readlines()
print(train)
count_wm = countvectorizer.fit_transform(train)
tfidf_wm = tfidfvectorizer.fit_transform(train)

count_tokens = countvectorizer.get_feature_names()
tfidf_tokens = tfidfvectorizer.get_feature_names()

df_countvect = pd.DataFrame(data = count_wm.toarray(), index = ['Doc1', 'Doc2'],
                            columns = count_tokens)
df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(), index = ['Doc1', 'Doc2'],
                            columns = count_tokens)

print("count Vectorizer\n")
print(df_countvect)

print("\nTD-IDF-Vectorizer\n")
print(df_tfidfvect)

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
    df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(), index = column_headers,
                            columns = tfidf_tokens)

    return df_tfidfvect
