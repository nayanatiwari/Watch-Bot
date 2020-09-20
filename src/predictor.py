import generate_model
import os
import glob
from data_util import get_data_from_jsonfile
from src import tfidf
"""
this file contains functions used to compare a document against a pre-existing
model stored in models/ .

if you want to generate a model, look at the file generate_model
"""
"""
available models for get_prediction(model_text...

naivebayes
complementbayes
gaussiannaivebayes
"""

MODEL_DIR = "models/"
SUPPORTED_COMBOS = ["naivebayes", "complementnaivebayes"]
MODEL_SUFF = ".model"

def get_prediction(model_text, documents=[], data_fname="", probs=False):
    if model_text == "combo":
        return get_combine_prediction(documents)
    model_file = MODEL_DIR + model_text + MODEL_SUFF
    matrix_file = model_file[:-6] + ".matrix"
    model, matrix = generate_model.load_model_and_matrix(model_file, matrix_file)
    if documents == [] and data_fname == "":
        print("No data passed for prediction")
    elif documents == []:
        data_fname = "" 
        while not os.path.isfile("data/" + data_fname  + ".json"):
            data_fname = input("Enter name of data json file in data/ with no .json suffix: ")
        
        documents = get_data_from_jsonfile(data_fname)

    predictions = predict_group(model, documents, matrix)

    return predictions

def predict_probability_doc(model, doc, tfidf_vect):
    vectorized_doc, tfidf_vect = tfidf.generate_tfidf_matrix([doc], test=True, tfidf_vect=tfidf_vect)
    try:
        return model.predict_proba(vectorized_doc)
    except TypeError:
        return model.predict_proba(vectorized_doc.toarray())

"""
only supports single document checks for now
"""
def get_combined_prediction(document):
    prediction_probabilities = []

    for classifier in SUPPORTED_COMBOS:
        model_file = MODEL_DIR + model_text + MODEL_SUFF
        matrix_file = model_file[:-6] + ".matrix"
        model, matrix = generate_model.load_model_and_matrix(model_file, matrix_file)
        prediction_probabilities.append(prediction_probability_doc(model, document[0], matrix))
    
    avg = [0 for _ in range(len(prediction_probabilities))]

    for i in range(len(prediction_probabilites)): 
        avg[0] += prediction_probabilities[i][0]
        avg[1] += prediction_probabilities[i][1]

    avg[0] = avg[0] / len(prediction_probabilites)
    avg[1] = avg[1] / len(prediction_probabilites)

    return 0 if avg[0] >= avg[1] else 1

"""
model: scikit-learn model
test_data: list of docs to generate predictions for
tfidf_vect: scikit-learn fit matrix for model
"""
def predict_group(model, test_data, tfidf_vect):
    vectorized_test_data, tfidf_vect = tfidf.generate_tfidf_matrix(test_data, test=True, tfidf_vect=tfidf_vect)
    print("Test data dims: {0}".format(vectorized_test_data.shape))

    # try except since gaussian and monomial require data in different forms
    try:
        predicted = model.predict(vectorized_test_data)
    except TypeError:
        predicted = model.predict(vectorized_test_data.toarray())
    return predicted

def predict_individual_doc(model, doc, tfidf_vect):
    vectorized_doc, tfidf_vect = tfidf.generate_tfidf_matrix([doc], test=True, tfidf_vect=tfidf_vect)
    try:
        return model.predict(vectorized_doc)
    except TypeError:
        return model.predict(vectorized_doc.toarray())

if __name__ == "__main__":
    print("WatchDog Predictor")
    models = glob.glob("models/*.model")
    if models != []:
        print("Found the following models: {0}".format(models))
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
        model, matrix = generate_model.load_model_and_matrix(model_file, matrix_file)
        data_fname = "" 
        while not os.path.isfile("data/" + data_fname  + ".json"):
            data_fname = input("Enter name of data json file in data/ with no .json suffix: ")
        
        data = get_data_from_jsonfile(data_fname)

        predictions = predict_group(model, data, matrix)
        
    else:
        print("No models found, please generate one generate_model.py")
        
