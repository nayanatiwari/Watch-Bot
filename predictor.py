import generate_model
import os
import glob
from data_util import get_data_from_jsonfile
import tfidf
"""
this file contains functions used to compare a document against a pre-existing
model stored in models/ .

if you want to generate a model, look at the file generate_model
"""
"""
available models for get_prediction(model_text...

naivebayes
"""

MODEL_DIR = "models/"
MODEL_SUFF = ".model"

def get_prediction(model_text, documents=[], data_fname=""):
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


"""
model: scikit-learn model
test_data: list of docs to generate predictions for
tfidf_vect: scikit-learn fit matrix for model
"""
def predict_group(model, test_data, tfidf_vect):
    vectorized_test_data, tfidf_vect = tfidf.generate_tfidf_matrix(test_data, test=True, tfidf_vect=tfidf_vect)
    print("Test data dims: {0}".format(vectorized_test_data.shape))
    predicted = model.predict(vectorized_test_data)
    return predicted

def predict_individual_doc(model, doc, tfidf_vect):
    vectorized_doc, tfidf_vect = tfidf.generate_tfidf_matrix([doc], test=True, tfidf_vect=tfidf_vect)
    return model.predict(vectorized_doc)

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
        



