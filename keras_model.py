import tensorflow as tf
import keras
from keras.activations import relu
from keras.layers import Input, Embedding, LSTM, Dense, Activation, Dense

print("Tensorflow version", tf.__version__)
print("Keras version", keras.__version__)


def ml_model(sentences, true_labels):
    """
    args:
        sentences: list of strings
        true_labels: list of true labels (True/False array)
    """
    sentences = tf.constant(sentences)
    is_question = tf.constant(true_labels)

    # Preprocess the input strings.
    hash_buckets = 1000
    words = tf.strings.split(sentences, ' ')
    hashed_words = tf.strings.to_hash_bucket_fast(words, hash_buckets)

    # Build the Keras model.
    keras_model = keras.Sequential([
        Input(shape=[None], dtype=tf.int64, ragged=True),
        Embedding(hash_buckets, 16),
        LSTM(32, use_bias=False),
        Dense(32),
        Activation(relu),
        Dense(1)
    ])

    keras_model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    keras_model.fit(hashed_words, is_question, epochs=200)
    print(keras_model.predict(hashed_words))


sentences = [
    "hello",
    "goodbye",
]
labels = [True, False]

ml_model(sentences, labels)
