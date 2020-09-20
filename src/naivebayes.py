from src import tfidf
import copy
import random
import src.data_util
from sklearn.naive_bayes import MultinomialNB

# 1 == suicidal
# 0 == not
S_FNAME = "/data/suicidal_data.txt"
N_FNAME = "/data/suicidal_data.txt"
T_T_SPLIT = .5  # proportion of data used for training
 
def generate_naive_bayes_model(train_data, train_labels):
  
    vectorized_train_data, tfidf_vect = tfidf.generate_tfidf_matrix(train_data)
    print("Train data dims: {0}".format(vectorized_train_data.shape))
    nb_model = MultinomialNB()
    nb_model.fit(vectorized_train_data, train_labels)
    return nb_model, tfidf_vect

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

    print("Total proportion correct of test group: {0}".format(sum_correct / len(test_labels))) 
   
    other_test_labels = []
    for i in range(len(test_data)):
        other_test_labels.append(predict_individual_doc(nb_model, test_data[i], tfidf_vect))

    sum_correct = 0
    for i, label in enumerate(other_test_labels):
        if label == test_labels[i]:
            sum_correct += 1
    



