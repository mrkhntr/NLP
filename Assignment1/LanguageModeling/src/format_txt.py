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

def add_newlines():
    training_set_path = os.getcwd() + '/trigram_counts.txt'

    format_file(training_set_path)
    f = open(training_set_path)
    f.close()

# add_newlines()