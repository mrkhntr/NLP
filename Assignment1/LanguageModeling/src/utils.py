import io
import os

training_set_path = os.getcwd() + '/gutenberg/'
training_files = os.listdir(training_set_path)


def translate_to_unk(char, unigram):
    if unigram.get(char) is None:
        return '?'
    return char


def training_set_to_str():
    training_corpus = ''
    for filename in training_files:
        with open(training_set_path + filename, 'r', encoding='iso-8859-15') as cur_file:
            training_corpus = training_corpus + cur_file.read()
    return training_corpus


def file_to_str(filepath):
    with io.open(filepath, 'r', encoding='iso-8859-15') as f:
        text = f.read()
    return text


def write_to_filepath(text, filepath):
    with io.open(filepath, 'w', encoding='iso-8859-15') as f:
        f.write(text)
