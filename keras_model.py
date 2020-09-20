import keras
import numpy as np
import tensorflow as tf
from keras import Model
from keras import backend as K
from keras.activations import relu
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.layers import (LSTM, Activation, Add, BatchNormalization,
                          Concatenate, Conv1D, Dense, Dropout, Embedding,
                          Flatten, GlobalAvgPool1D, GlobalMaxPool1D, Input,
                          Lambda, MaxPool1D, ReLU, Reshape, UpSampling1D,
                          ZeroPadding1D)
from keras.optimizers import Adam

NUM_HASH_BUCKETS = 10_000

def make_hash_words(sentences):
    words = tf.strings.split(sentences, ' ')
    return tf.strings.to_hash_bucket_fast(words, NUM_HASH_BUCKETS)


class OurModel():

    def __init__(self, sentences, target_labels, args):
        """
        args:
            sentences: list of strings
            true_labels: list of true labels (True/False array)
        """
        global NUM_HASH_BUCKETS
        self.data_len = len(target_labels)
        self.sentences = tf.constant(sentences)
        self.target_labels = tf.constant(target_labels)
        self.args = args

        # Preprocess the input strings.
        self.hash_buckets = NUM_HASH_BUCKETS
        self.hashed_words = make_hash_words(sentences)
        
        self.make_model()

        self.model.compile(
            loss='binary_crossentropy', 
            optimizer=Adam(0.001)
        )

        self.model.summary()

        # manual validation split
        split = round(self.data_len * 0.3)
        self.x = self.hashed_words[:-split]
        self.y = self.target_labels[:-split]
        self.valx = self.hashed_words[-split:]
        self.valy = self.target_labels[-split:]

    def make_model(self):
        name = self.args.modelname

        if name == "original":
            inpt = Input(shape=[None], dtype=tf.int64, ragged=True)
            x = Embedding(self.hash_buckets, 16)(inpt)
            x = LSTM(32, use_bias=False)(x)
            x = Dense(32)(x)
            x = Activation(relu)(x)
            x = Dense(1)(x)
            self.model = Model(inpt, x)
        
        elif name == "bigdense":
            inpt = Input(shape=[None], dtype=tf.int64, ragged=True)
            x = Embedding(self.hash_buckets, 128)(inpt)
            x = Dense(256)(x)
            x = ReLU()(x)
            x = Dense(128)
            x = ReLU()(x)
            x = Dense(32)
            x = ReLU()(x)
            x = Dense(1)(x)

            self.model = Model(inpt, x)

        elif name == "conv":
            inpt = Input(shape=[None], dtype=tf.int64, ragged=True)
            x = Embedding(self.hash_buckets, 16)(inpt)
            x = Conv1D(32, 7, padding="valid")(x)
            x = ReLU()(x)
            x = MaxPool1D(8)(x)
            x = Conv1D(32, 7, padding="valid")(x)

            self.model = Model(inpt, x)

        elif name == "sentiment":
            inpt = Input(shape=[None], dtype=tf.int64, ragged=True)
            inpt2 = Input(shape=[None], dtype=tf.int64, ragged=True)
            x = Embedding(self.hash_buckets, 16)(inpt)
            x = Conv1D(32, 7, padding="valid")(x)
            x = ReLU()(x)
            x = MaxPool1D(8)(x)
            x = Conv1D(32, 7, padding="valid")(x)

            self.model = Model(inpt, x)

        else:
            raise ValueError("No model found named '" + str(name) + "'")
    
        self.model # to check it is defined now


    def train(self):
        """
        the range (confidence, 1-confidence) will be treated as "uncertain results"
        """
        # callbacks
        callbacks = [
            ModelCheckpoint("models/" + self.args.name + "_best_val_loss.hdf5", verbose=1, save_best_only=True, save_freq="epoch"),
            ReduceLROnPlateau(patience=self.args.epochs//5)
        ]

        # fitting
        try:
            self.model.fit(
                x=self.x,
                y=self.y,
                validation_data=(self.valx, self.valy),
                epochs=self.args.epochs,
                batch_size=self.args.batchsize,
                validation_batch_size=self.args.batchsize,
                verbose=1,
                callbacks=callbacks,
            )
        except KeyboardInterrupt:
            print("\nManual early stop...")
        
        self.model.save("models/" + self.args.name + "_final.hdf5")


    def test(self, inputs, targets, name, confidence=0.3):
        predicts = np.squeeze(self.model.predict(inputs))
        targets = K.eval(targets)

        correct_neg = 1 - targets[predicts < confidence]
        correct_pos = targets[predicts > (1-confidence)]
        correct = np.sum(correct_pos) + np.sum(correct_neg)
        uncertain = np.sum(
            np.logical_and(
                (predicts >= confidence),
                (predicts <= (1-confidence))
            )
        )
        print("\n" + name.title())
        print(correct, "correct out of", len(targets))
        print(correct/len(targets))
        print(uncertain, "uncertain")


