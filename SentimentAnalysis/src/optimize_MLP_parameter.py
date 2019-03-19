import numpy
import import_data as data
import numpy as np
import pandas as pd
from tensorflow.python import keras
import tensorflow as tf
import sys
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


word_index_dict = data.word_index_dictionary()
VOCAB_SIZE = len(word_index_dict)
df, VECTOR_LEN = data.encode_train_data(word_index_dict)
df = df.sample(frac=1)


def convert_lol_to_numpy(lol):
    rol = []
    for l in lol:
        rol.append(numpy.array(l))
    return numpy.array(rol)


def partition_training(training_df):
    partition = int(len(training_df) / 7)
    held_out_train = training_df.iloc[0:partition]
    train_data = training_df.iloc[partition:]
    return train_data, held_out_train


def gen_model(first_hidden_layer, activation_func):

    model = MLPClassifier(hidden_layer_sizes=(first_hidden_layer, 10), max_iter=500, alpha=0.0001,
                          activation=activation_func, solver='adam', verbose=10, random_state=21, tol=0.000000001)

    return model


def cross_validate_model(first_hidden_layer, ac_fun):
    chunks = np.array_split(df, 10)
    max_acc = -sys.maxsize
    sum_acc = 0
    num_acc = 0
    for i in range(0, 1):
        test = chunks[i]
        train = pd.DataFrame()
        for j in range(0, len(chunks)):
            if j != i:
                train = pd.concat([train, chunks[j]])

        x_train = convert_lol_to_numpy(train['Encoded Review'])
        y_train = numpy.array(train['Class'])

        x_test = convert_lol_to_numpy(test['Encoded Review'])
        y_test = numpy.array(test['Class'])

        model = gen_model(first_hidden_layer, ac_fun)

        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        score = accuracy_score(y_test, y_pred)

        acc = score
        if acc > max_acc:
            max_acc = acc
        sum_acc += acc
        num_acc += 1
    mean_acc = sum_acc / num_acc
    return max_acc, mean_acc


def optimize_params():
    max_acc, mean_acc = cross_validate_model(6, 'relu')
    print(max_acc)
    print(mean_acc)


def main():
    optimize_params()
    # sk_learn_MLP()


main()
