import copy
import os.path
import random

from joblib import dump, load
from sklearn.metrics import precision_score, recall_score

from src import data_util
import predictor
from src.complementnaivebayes import generate_complement_naive_bayes_model
from src.gaussianbayes import generate_gaussian_naive_bayes_model
from src.naivebayes import generate_naive_bayes_model

models = ["models/naivebayes.model", "models/gaussiannaivebayes.model", "models/complementnaivebayes.model" ,"combo"]
matrices = ["models/naivebayes.matrix", "models/gaussiannaivebayes.matrix", "models/complementnaivebayes.model"]

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

def generate_and_save_model(model_file, matrix_file, being_combined=False):

    classifier_to_use = os.path.basename(model_file).split(".")[0]
    tr_s_d, tr_n_d, te_s_d, te_n_d = get_split_data(T_T_SPLIT)
    train_labels, test_labels = get_data_labels(tr_s_d, tr_n_d, te_s_d, te_n_d)
    train_data = tr_s_d + tr_n_d
    test_data = te_s_d + te_n_d

    if classifier_to_use == "naivebayes":
        nb_model, tfidf_vect  = generate_naive_bayes_model(train_data, train_labels)
    elif classifier_to_use == "complementnaivebayes":
        nb_model, tfidf_vect  = generate_complement_naive_bayes_model(train_data, train_labels)
    elif "gaussiannaivebayes" in classifier_to_use:
            nb_model, tfidf_vect  = generate_gaussian_naive_bayes_model(train_data, train_labels)

    else:
        print("Invalid model type: {0}".format(classifier_to_use))
        exit()
    
    dump(nb_model, model_file)
    dump(tfidf_vect, matrix_file)
  

    correct = 0
    predictions = []
    for doc in test_data:
        predictions.append(predictor.predict_individual_doc(nb_model, doc, tfidf_vect)) 
    for i, label in enumerate(predictions):
        if label == test_labels[i]:
            correct += 1

    print("Percentage correct for new model {0}: {1}".format(model_file, correct/len(test_labels)))
    print("Precision score: {0}: {1}".format(model_file, precision_score(test_labels, predictions)))
    print("Recall score: {0}: {1}".format(model_file, recall_score(test_labels, predictions)))

def generate_and_save_combo():
    tr_s_d, tr_n_d, te_s_d, te_n_d = get_split_data(T_T_SPLIT)
    train_labels, test_labels = get_data_labels(tr_s_d, tr_n_d, te_s_d, te_n_d)
    train_data = tr_s_d + tr_n_d
    test_data = te_s_d + te_n_d

    prediction_probs = []

    for i, model in enumerate(models):
        if "complementnaivebayes" in model:
            nb_model, tfidf_vect  = generate_complement_naive_bayes_model(train_data, train_labels)
        elif "naivebayes" in model and not "gaussian" in model: #hacky and shite
            nb_model, tfidf_vect  = generate_naive_bayes_model(train_data, train_labels)
        else:
            continue

        prediction_probabs = []
        for doc in test_data:
            prediction_probabs.append(predictor.predict_probability_doc(nb_model, doc, tfidf_vect)[0])

        prediction_probs.append(prediction_probabs)

    prediction = []
    for j in range(len(prediction_probs[0])):
        avg = [0 for _ in range(len(prediction_probs[0][0]))]
        for i in range(len(prediction_probs)):
            for k in range(len(prediction_probs[0][0])):
                avg[k] += prediction_probs[i][j][k]

        for k in range(len(avg)):
            avg[k] = avg[k] / len(prediction_probs[0])
        
        prediction.append(0 if avg[0] >= avg[1] else 1)

    correct = 0
    for i, label in enumerate(prediction):
        if label == test_labels[i]:
            correct += 1

    print("Percentage correct for combined models: {0}".format(correct/len(test_labels)))

def load_model_and_matrix(model_file, matrix_file):
    if not os.path.isfile(model_file) or not os.path.isfile(matrix_file):
        print("no model file")
        exit()
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

    if models[i] == "combo":
        generate_and_save_combo()

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
