import tfidf
import copy
import random
import data_util
from sklearn.naive_bayes import MultinomialNB

# 1 == suicidal
# 0 == not
S_FNAME = "/data/suicidal_data.txt"
N_FNAME = "/data/suicidal_data.txt"
T_T_SPLIT = .5  # proportion of data used for training

def get_data_as_list_of_documents():
    suicidal_docs, not_docs = data_util.get_data_from_directory() 
    return suicidal_docs, not_docs

def split_docs_train_test(docs, train_test_split):
    # create copy of docs so og list of data stays fine
    docs_copy = copy.deepcopy(docs)
    train_count = int(len(docs) * train_test_split)
    train_docs = []

    # remove train_count docs from docs_copy and add them to train_docs
    for i in range(train_count):
        train_docs.append(docs_copy.pop(random.randrange(len(docs_copy))))
    
    return train_docs, docs_copy

def get_split_data(suicidal_fname, not_fname, train_test_split):
    suicidal_docs, not_docs = get_data_as_list_of_documents()
    train_suicidal_docs, test_suicidal_docs =\
                                split_docs_train_test(suicidal_docs,
                                                    train_test_split)

    train_not_docs, test_not_docs =\
                                split_docs_train_test(not_docs,
                                                    train_test_split)

    return train_suicidal_docs, train_not_docs, test_suicidal_docs, test_not_docs

def get_data_labels(tr_s_d, tr_n_d, te_s_d, te_n_d):
    train_labels = [1 for _ in range(len(tr_s_d))] + [0 for _ in range(len(tr_n_d))]
    test_labels = [1 for _ in range(len(te_s_d))] + [0 for _ in range(len(te_n_d))]

    return train_labels, test_labels
    
def generate_naive_bayes_model(train_data, train_labels):
  
    vectorized_train_data, tfidf_vect = tfidf.generate_tfidf_matrix(train_data)
    print("Train data dims: {0}".format(vectorized_train_data.shape))
    nb_model = MultinomialNB()
    nb_model.fit(vectorized_train_data, train_labels)
    return nb_model, tfidf_vect

def predict_based_on_model(model, test_data, tfidf_vect):
    vectorized_test_data, tfidf_vect = tfidf.generate_tfidf_matrix(test_data, test=True, tfidf_vect=tfidf_vect)
    print("Test data dims: {0}".format(vectorized_test_data.shape))
    predicted = model.predict(vectorized_test_data)
    return predicted

if __name__ == "__main__":
    tr_s_d, tr_n_d, te_s_d, te_n_d = get_split_data(S_FNAME, N_FNAME, T_T_SPLIT)
    train_labels, test_labels = get_data_labels(tr_s_d, tr_n_d, te_s_d, te_n_d)
    train_data = tr_s_d + tr_n_d
    test_data = te_s_d + te_n_d

    # using count_vect to keep track of shape of trained model
    nb_model, tfidf_vect = generate_naive_bayes_model(train_data, train_labels)
    predicted_test_labels = predict_based_on_model(nb_model, test_data, tfidf_vect)

    sum_correct = 0
    for i, label in enumerate(predicted_test_labels):
        if label == test_labels[i]:
            sum_correct += 1

    print("Total proportion correct: {0}".format(sum_correct / len(test_labels)))
 
