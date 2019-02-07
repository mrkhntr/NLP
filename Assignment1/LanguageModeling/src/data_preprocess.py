# -*- coding: utf-8 -*-
import fileinput
import os
from collections import Counter

def replace_unk(line):
    unk = ['\x1a', '\xe6', '\xe9', '\xe8', '\xee', '\xef', '\xbd', '\xbf']
    if any(s in line for s in unk):
        for sym in unk:
            line = line.replace(sym, '?')
    return line


def format_line(line):
    punctuation = ',.-";\'!_?:`)(&[]*}/$%>@<+=~'

    line = line.rstrip()  # remove blank lines
    line = ' '.join(line.split())  # remove duplicate spaces
    line = line.translate(None, punctuation)  # remove punctuation
    line = replace_unk(line)
    return line


def format_file(filename):
    for line in fileinput.FileInput(filename, inplace=1):
        line = format_line(line)
        if line:
            print line,  # remove newline characters

# TODO: First data_preprocess, then count_ngram and print to file,
# TODO:      and finally, format each file into json format
def data_preprocess():
    training_set_path = os.getcwd() + '/gutenberg/'
    file_names = os.listdir(training_set_path)

    unigram = Counter()
    for filename in file_names:
        format_file(training_set_path + filename)
        f = open(training_set_path + filename)
        unigram += Counter(f.read().strip())
        f.close()

    return unigram

