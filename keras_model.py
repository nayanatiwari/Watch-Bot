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

print(tf.__version__)
print(keras.__version__)


NUM_HASH_BUCKETS = 10_000

def make_hash_words(sentences):
    words = tf.strings.split(sentences, ' ')
    return tf.strings.to_hash_bucket_fast(words, NUM_HASH_BUCKETS)


class OurModel():

    def __init__(self, sentences, target_labels, sent_emot, args):
        """
        args:
            sentences: list of strings
            true_labels: list of true labels (True/False array)
            sent_emot: sentiment/emotion vectors
        """
        global NUM_HASH_BUCKETS
        self.data_len = len(target_labels)
        self.sentences = tf.constant(sentences)
        self.target_labels = tf.constant(target_labels)
        self.sent_emot = tf.constant(sent_emot)
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

        x = self.hashed_words[:-split]
        sentemot_x = self.sent_emot[:-split]
        valx = self.hashed_words[-split:]
        val_sentemot_x = self.sent_emot[-split:]

        if self.uses_sentiment:
            self.x = [x, sentemot_x]
            self.valx = [valx, val_sentemot_x]
        else:
            self.x = x
            self.valx = valx

        self.y = self.target_labels[:-split]
        self.valy = self.target_labels[-split:]


    def make_model(self):
        name = self.args.modelname

        self.uses_sentiment = False

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
            x = Embedding(self.hash_buckets, 32)(inpt)
            x = LSTM(256)(x)
            x = Dense(256)(x)
            x = ReLU()(x)
            x = Dense(128)(x)
            x = ReLU()(x)
            x = Dense(32)(x)
            x = ReLU()(x)
            x = Dense(1)(x)

            self.model = Model(inpt, x)

        elif name == "conv":
            inpt = Input(shape=[None], dtype=tf.int64, ragged=True)
            x = Embedding(self.hash_buckets, 32)(inpt)
            x = LSTM(128)(x)
            x = Reshape((128,1))(x)
            x = Conv1D(128, 7, padding="valid")(x)
            x = ReLU()(x)
            x = MaxPool1D(2)(x)
            x = Conv1D(64, 7, padding="valid")(x)
            x = MaxPool1D(2)(x)
            x = Conv1D(16, 5, padding="valid")(x)
            x = GlobalMaxPool1D()(x)
            x = Dense(1)(x)

            self.model = Model(inpt, x)

        elif name == "sentiment":
            self.uses_sentiment = True

            inpt = Input(shape=[None], dtype=tf.int64, ragged=True)
            sent_inpt = Input(shape=[6])

            s = Dense(16)(sent_inpt)
            s = Activation("tanh")(s)
            s = Dense(6)(s)
            s = Activation("tanh")(s)
            s = Dense(1)(s)

            # just big dense
            x = Embedding(self.hash_buckets, 32)(inpt)
            x = LSTM(256)(x)
            x = Dense(256)(x)
            x = ReLU()(x)
            x = Dense(128)(x)
            x = ReLU()(x)
            x = Dense(32)(x)
            x = ReLU()(x)
            x = Dense(1)(x)

            x = Concatenate()([x, s])
            x = Dense(16)(x)
            x = Activation("tanh")(x)
            x = Dense(1)(x)

            self.model = Model([inpt, sent_inpt], x)

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


    def test(self, inputs, targets, name, confidence=0.5):
        """
        confidence: between 0 (very strict) and 0.5 (0.49 will become 0)
        """
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


