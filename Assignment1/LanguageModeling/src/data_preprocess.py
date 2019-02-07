# -*- coding: utf-8 -*-
import fileinput
import os


def replace_unk(line):
    unk = ['\x1a', '\xe6', '\xe9', '\xe8', '\xee', '\xef', '\xbd', '\xbf']
    if any(s in line for s in unk):
        for sym in unk:
            line = line.replace(sym, '?')
    return line


# TODO: Get rid of random unicode characters from unigram
def format_line(line):
    punctuation = ',.-";\'!_?:`)(&[]*}/$%>@<+=~'
    # unicode_chars = ['\x00', '\xff', '\x01', '\x10']

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


def data_preprocess():
    training_set_path = os.getcwd() + '/gutenberg/'
    file_names = os.listdir(training_set_path)

    for filename in file_names:
        format_file(training_set_path + filename)
        f = open(training_set_path + filename)
        f.close()


data_preprocess()