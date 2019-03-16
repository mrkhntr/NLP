import utils
from collections import defaultdict
import pandas as pd


def word_index_dictionary():
    word_index = 2
    word_index_dict = defaultdict(lambda: 1, {})
    word_index_dict["<PAD>"] = 0
    word_index_dict["<UNK>"] = 1  # unknown

    for filename in utils.pos_training_files:
        file_str = utils.file_to_str(utils.pos_training_set_path + filename)
        word_index = add_word_list_to_dictionary(file_str.split(), word_index_dict, word_index)

    for filename in utils.neg_training_files:
        file_str = utils.file_to_str(utils.neg_training_set_path + filename)
        word_index = add_word_list_to_dictionary(file_str.split(), word_index_dict, word_index)

    return word_index_dict


def get_max_review_len():
    max_train_len = -1
    for filename in utils.pos_training_files:
        file_str = utils.file_to_str(utils.pos_training_set_path + filename)
        num_words = len(file_str.split())
        if num_words > max_train_len:
            max_train_len = num_words

    for filename in utils.neg_training_files:
        file_str = utils.file_to_str(utils.neg_training_set_path + filename)
        num_words = len(file_str.split())
        if num_words > max_train_len:
            max_train_len = num_words

    print(max_train_len)
    return max_train_len


def encode_train_data(word_index_dict):
    max_train_len = get_max_review_len()
    d = []

    for filename in utils.pos_training_files:
        file_enc = []
        file_str = utils.file_to_str(utils.pos_training_set_path + filename)
        for word in file_str.split():
            file_enc.append(word_index_dict[word])
        utils.pad_array(file_enc, max_train_len, word_index_dict["<PAD>"])
        d.append((file_enc, 1))

    for filename in utils.neg_training_files:
        file_enc = []
        file_str = utils.file_to_str(utils.neg_training_set_path + filename)
        for word in file_str.split():
            file_enc.append(word_index_dict[word])
        utils.pad_array(file_enc, max_train_len, word_index_dict["<PAD>"])
        d.append((file_enc, -1))

    df = pd.DataFrame(d, columns=('Encoded Review', 'Class'))

    return df


def add_word_list_to_dictionary(l, dictionary, word_index):
    for item in l:
        if item not in dictionary:
            dictionary[item] = word_index
            word_index += 1
    return word_index


def main():
    word_index_dict = word_index_dictionary()
    df = encode_train_data(word_index_dict)

    utils.write_to_filepath(str(df), 'df.txt')


main()
