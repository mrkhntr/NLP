# -*- coding: utf-8 -*-
import fileinput
import os
from collections import Counter

def format_line(line):
    line = line.replace(',', ',\n')
    return line


def format_file(filename):
    for line in fileinput.FileInput(filename, inplace=1):
        line = format_line(line)
        print line

def data_preprocess():
    training_set_path = os.getcwd() + '/bigram_counts.txt'

    format_file(training_set_path)
    f = open(training_set_path)
    f.close()

# data_preprocess()