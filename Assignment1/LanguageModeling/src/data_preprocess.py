import fileinput
import os
from collections import Counter


def format_line(line):
    punctuation = ',.-";\'!_?:`)(&[]*}/$%>@<+=~'

    line = line.rstrip()  # remove blank lines
    line = ' '.join(line.split())  # remove duplicate spaces
    line = line.translate(None, punctuation)  # remove punctuation
    return line

def format_file(filename):
    for line in fileinput.FileInput(filename, inplace=1):
        line = format_line(line)
        if line:
            print line,  # remove newline characters

def data_preprocess():
    training_set_path = '/Users/raihans/Northeastern/Spring2019/NLP/Assignment1/LanguageModeling/gutenberg/'
    file_names = os.listdir(training_set_path)

    c = Counter()
    for filename in file_names:
        format_file(training_set_path + filename)
        f = open(training_set_path + filename)
        c += Counter(f.read().strip())
        f.close()

    print c

data_preprocess()

