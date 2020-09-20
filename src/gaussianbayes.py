from src import tfidf
from sklearn.naive_bayes import GaussianNB

def generate_gaussian_naive_bayes_model(train_data, train_labels):
  
    vectorized_train_data, tfidf_vect = tfidf.generate_tfidf_matrix(train_data)
    print("Train data dims: {0}".format(vectorized_train_data.shape))
    nb_model = GaussianNB()
    nb_model.fit(vectorized_train_data.toarray(), train_labels)
    return nb_model, tfidf_vect
