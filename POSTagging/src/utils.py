import io
import os
import operator
import sys

training_set_path = os.getcwd() + '/brown/'
training_files = os.listdir(training_set_path)
count_output_path = os.getcwd() + '/all_counts/'
probabilities_path = os.getcwd() + '/all_probabilities/'


def max_value_key(dictionary):
    return max(dictionary.items(), key=operator.itemgetter(1))[0]


# referenced https://stackoverflow.com/questions
#            /23862406/filter-items-in-a-python-dictionary-where-keys-contain-a-specific-string
def dict_items_with_substring(substring, dict):
    return {k: v for (k, v) in dict.items() if substring in k}


def increment_dict(key, dictionary, increment):
    if key not in dictionary:
        dictionary[key] = increment
    else:
        dictionary[key] += increment


def training_set_to_str():
    training_corpus = ''
    for filename in training_files:
        with open(training_set_path + filename, 'r', encoding='iso-8859-15') as cur_file:
            training_corpus = training_corpus + '\n' + cur_file.read()
    return training_corpus


def file_to_str(filepath):
    with io.open(filepath, 'r', encoding='iso-8859-15') as f:
        text = f.read()
    return text


def write_to_filepath(text, filepath):
    with io.open(filepath, 'w', encoding='iso-8859-15') as f:
        f.write(text)


def print_dict_to_file(dict, filepath):
    with io.open(filepath, 'w', encoding='iso-8859-15') as f:
        for key in list(dict.keys()):
            f.write("\"" + key + "\"" + ": " + str(dict[key]) + "\n")
