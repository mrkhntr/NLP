# -*- coding: utf-8 -*-
import fileinput
import os


#  ? will be known as our <unk>
def replace_unk(line):
    unk = ['\x98', '\x85', '\x12', '\xa9', '\x18', '\x16', '\xf3', '\x0f', '\x13',
           '\xe8', '\x1a', '\xe9', '\x15', '\xe6', '\x14', '\x03' '\x11', '\xee', '\x11',
           '\x03']
    if any(s in line for s in unk):
        for sym in unk:
            line = line.replace(sym, '?')
    return line


def format_line(line):
    punctuation = ',.-";\'!_?:`)(&[]*}/$%>@<+=~\r'

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
