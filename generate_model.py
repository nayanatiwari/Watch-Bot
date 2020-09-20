import os.path
import data_util
import copy
import random
from naivebayes import generate_naive_bayes_model
from joblib import dump, load

model_file = "models/naivebayes.model"
matrix_file = "models/naivebayes.matrix"

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

def generate_and_save_model():

    tr_s_d, tr_n_d, te_s_d, te_n_d = get_split_data(S_FNAME, N_FNAME, T_T_SPLIT)
    train_labels, test_labels = get_data_labels(tr_s_d, tr_n_d, te_s_d, te_n_d)
    train_data = tr_s_d + tr_n_d
    test_data = te_s_d + te_n_d

    nb_model, tfidf_vect  = generate_naive_bayes_model(train_data, train_labels)
    
    dump(nb_model, model_file)
    dump(tfidf_vect, matrix_file)

def load_model_and_matrix(model_file, matrix_file):
    model = load(model_file)
    matrix = load(matrix_file)

    return model, matrix

def predict_based_on_model(model, test_data, tfidf_vect):
    vectorized_test_data, tfidf_vect = tfidf.generate_tfidf_matrix(test_data, test=True, tfidf_vect=tfidf_vect)
    print("Test data dims: {0}".format(vectorized_test_data.shape))
    predicted = model.predict(vectorized_test_data)
    return predicted

def predict_individual_doc(model, doc, tfidf_vect):
    vectorized_doc, tfidf_vect = tfidf.generate_tfidf_matrix([doc], test=True, tfidf_vect=tfidf_vect)
    return model.predict(vectorized_doc)

if __name__ == "__main__":

    if os.path.isfile(model_file):
        overwrite = input("A saved model ({0}) exists, overwrite? (y/n)".format(model_file))
        if overwrite == 'y':
            generate_and_save_model()
        else:
            load_model_and_matrix(model_file, matrix_file)
            exit()
    else:
        generate_and_save_model()


    
