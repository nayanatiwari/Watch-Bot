import os.path
import data_util
import copy
import random
import predictor
from naivebayes import generate_naive_bayes_model
from gaussianbayes import generate_gaussian_naive_bayes_model
from joblib import dump, load

models = ["models/naivebayes.model", "models/gaussiannaivebayes.model"]
matrices = ["models/naivebayes.matrix", "models/gaussiannaivebayes.matrix"]

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

def get_split_data(train_test_split):
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

def generate_and_save_model(model_file, matrix_file):

    classifier_to_use = os.path.basename(model_file).split(".")[0]
    tr_s_d, tr_n_d, te_s_d, te_n_d = get_split_data(T_T_SPLIT)
    train_labels, test_labels = get_data_labels(tr_s_d, tr_n_d, te_s_d, te_n_d)
    train_data = tr_s_d + tr_n_d
    test_data = te_s_d + te_n_d

    if classifier_to_use == "naivebayes":
        nb_model, tfidf_vect  = generate_naive_bayes_model(train_data, train_labels)
    elif classifier_to_use == "gaussiannaivebayes":
        nb_model, tfidf_vect  = generate_gaussian_naive_bayes_model(train_data, train_labels)
    else:
        print("Invalid model type: {0}".format(classifier_to_use))
        exit()
    
    dump(nb_model, model_file)
    dump(tfidf_vect, matrix_file)
    
    predictions = []
    for doc in test_data:
        predictions.append(predictor.predict_individual_doc(nb_model, doc, tfidf_vect))

    correct = 0
    for i, label in enumerate(predictions):
        if label == test_labels[i]:
            correct += 1

    print("Percentage correct for new model: {0}".format(correct/len(test_labels)))



def load_model_and_matrix(model_file, matrix_file):
    model = load(model_file)
    matrix = load(matrix_file)

    return model, matrix

if __name__ == "__main__":

    print("Models available to generate: {0}".format(models))
    index = ""
    while not index.isnumeric():
        index = input("Select your model by index: ")
        if not index.isnumeric():
            print("Invalid index, please enter an integer.")
        else:
            i = int(index)
            if i >= len(models):
                print("Index outside of range of model list.")

    model_file = models[i]
    matrix_file = model_file[:-6] + ".matrix"

    if os.path.isfile(model_file):
        overwrite = input("A saved model ({0}) exists, overwrite? (y/n)".format(model_file))
        if overwrite == 'y':
            generate_and_save_model(model_file, matrix_file)
        else:
            load_model_and_matrix(model_file, matrix_file)
            exit()
    else:
        generate_and_save_model(model_file, matrix_file)


    
