from src import tfidf
import copy
import random
import data_util
from sklearn.naive_bayes import ComplementNB

def generate_complement_naive_bayes_model(train_data, train_labels):
  
    vectorized_train_data, tfidf_vect = tfidf.generate_tfidf_matrix(train_data)
    print("Train data dims: {0}".format(vectorized_train_data.shape))
    nb_model = ComplementNB()
    nb_model.fit(vectorized_train_data, train_labels)
    return nb_model, tfidf_vect
