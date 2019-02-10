# coding=iso-8859-15
import os
import io
import utils


#  ? will be known as our <unk>
def replace_unk(line):
    unk = ['\x98', '\x12', '©', '\x18', '\x16', 'æ', '\x0f', '\x15', 'ó', '\x13', '\x1a', 'è',
           'é', '\x11', '\x14', '\x03', 'î']
    if any(s in line for s in unk):
        for sym in unk:
            line = line.replace(sym, '?')
    return line


def format_line(line):
    punctuation = ',.-";\'!_?:`)(&[]*}/$%>@<+=~\r'

    line = line.rstrip()  # remove blank lines
    line = ' '.join(line.split())  # remove duplicate spaces
    remove_punc = str.maketrans('', '', punctuation)
    line = line.translate(remove_punc)  # remove punctuation
    line = replace_unk(line)
    return line


def format_file(filename):
    text = utils.file_to_str(filename)

    text = format_line(text)

    utils.write_to_filepath(text, filename)


def data_preprocess():
    training_set_path = os.getcwd() + '/gutenberg/'
    file_names = os.listdir(training_set_path)

    for filename in file_names:
        format_file(training_set_path + filename)


data_preprocess()
