import json
import os
import probability_ngram
from sklearn.model_selection import train_test_split

training_set_path = os.getcwd() + '/gutenberg/'
file_names = os.listdir(training_set_path)


def get_unigrams(train, unigram):
    unigram_probs = {}
    for sen in range(0, len(train)):
        for c in range(0, len(sen)):
            if c+1 != len(sen):
                text_and_prob = probability_ngram.unigram_prob(sen, c, unigram)
                cur_char = text_and_prob.get('text')
                new_prob = text_and_prob.get('prob')

                if cur_char in unigram_probs:
                    cur_prob = unigram_probs.get(cur_char)
                    unigram_probs.update({cur_char: cur_prob + new_prob})
                else:
                    unigram_probs.update({cur_char: new_prob})
    return unigram_probs

def main():
    with open(os.getcwd() + '/ngram_counts/unigram_counts.txt') as fh:
        unigram_counts = json.load(fh)

    with open(os.getcwd() + '/ngram_counts/bigram_counts.txt') as fh:
        bigrams_counts = json.load(fh)

    with open(os.getcwd() + '/ngram_counts/trigram_counts.txt') as fh:
        trigrams_counts = json.load(fh)

    data = []
    for filename in file_names:
        with open(training_set_path + filename, 'r') as cur_file:
            data = data + cur_file.read().split(".")

    train, test = train_test_split(data, test_size=0.2)

    train[0]