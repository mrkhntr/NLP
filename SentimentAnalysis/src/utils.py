import io
import os

pos_training_set_path = os.getcwd() + '/train/pos/'
pos_training_files = os.listdir(pos_training_set_path)
neg_training_set_path = os.getcwd() + '/train/neg/'
neg_training_files = os.listdir(neg_training_set_path)


def file_to_str(filepath):
    with io.open(filepath, 'r', encoding='iso-8859-15') as f:
        text = f.read()
    return text


def write_to_filepath(text, filepath):
    with io.open(filepath, 'w', encoding='iso-8859-15') as f:
        f.write(text)


def pad_array(array, max_len, pad):
    if len(array) < max_len:
        for i in range(0, max_len - len(array)):
            array.append(pad)
