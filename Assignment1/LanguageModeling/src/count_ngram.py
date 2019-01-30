import os
from collections import Counter
import fileinput
from itertools import izip, islice


def count_bigram(text):
    ngram_count = {}
    for c in range(0, len(text)):
        if c+1 != len(text):
            entry = ''
            entry += text[c] + text[c+1]

            if entry in ngram_count:
                ngram_count[entry] += 1
            else:
                ngram_count[entry] = 1

    print ngram_count
    return ngram_count

assert(count_bigram('ab') == {'ab': 1})
assert(count_bigram('abc') == {'ab': 1, 'bc': 1})

def main():

    # training_set_path = os.getcwd() + '/gutenberg/'
    # file_names = os.listdir(training_set_path)

    # unigram = Counter()
    # for filename in file_names:
    #    f = open(training_set_path + filename)
    #    unigram += Counter(f.read().strip())
    #    f.close()
    pass