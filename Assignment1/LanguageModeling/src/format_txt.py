# -*- coding: utf-8 -*-
import fileinput
import os

def format_line(line):
    line = line.replace(',', ',\n')
    line = line.replace("'", "\"")
    return line


def format_file(filename):
    for line in fileinput.FileInput(filename, inplace=1):
        line = format_line(line)
        print line,

def add_newlines_change_quotes():
    training_set_path = os.getcwd() + '/ngram_counts/trigram_counts.txt'
    format_file(training_set_path)
    f = open(training_set_path)
    f.close()

# add_newlines_change_quotes()