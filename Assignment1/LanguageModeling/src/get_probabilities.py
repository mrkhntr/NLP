# coding=iso-8859-15
import json
import os
import utils
import probability_ngram
import count_ngram
from sklearn.model_selection import train_test_split

training_set_path = os.getcwd() + '/gutenberg/'
file_names = os.listdir(training_set_path)
ngram_probability_path = os.getcwd() + '/ngram_probabilities/'


def print_json_ngram_to_file(ngram, filename):
    file_path = ngram_probability_path + filename

    utils.write_to_filepath(str(ngram), file_path)
    count_ngram.jsonify_file(file_path)


def get_ngram_probs(train, ngram_probability, trigram_counts, bigram_counts, unigram_counts):
    ngram_probs = {}
    for c in range(0, len(train)):
        if c+1 != len(train):
            if ngram_probability == probability_ngram.trigram_prob:
                text_and_prob = probability_ngram.trigram_prob(train, c, trigram_counts, bigram_counts, unigram_counts)
            elif ngram_probability == probability_ngram.bigram_prob:
                text_and_prob = probability_ngram.bigram_prob(train, c, bigram_counts, unigram_counts)
            else:
                text_and_prob = probability_ngram.unigram_prob(train, c, unigram_counts)

            cur_char = text_and_prob.get('text')
            new_prob = text_and_prob.get('prob')

            if cur_char in ngram_probs:
                cur_prob = ngram_probs.get(cur_char)
                ngram_probs.update({cur_char: cur_prob + new_prob})
            else:
                ngram_probs.update({cur_char: new_prob})

    return ngram_probs

def main():
    with open(os.getcwd() + '/ngram_counts/unigram_counts.txt', encoding='iso-8859-15') as fh:
        unigram_counts = json.load(fh)

    with open(os.getcwd() + '/ngram_counts/bigram_counts.txt', encoding='iso-8859-15') as fh:
        bigram_counts = json.load(fh)

    with open(os.getcwd() + '/ngram_counts/trigram_counts.txt', encoding='iso-8859-15') as fh:
        trigram_counts = json.load(fh)

    training_corpus = ''
    for filename in file_names:
        with open(training_set_path + filename, 'r', encoding='iso-8859-15') as cur_file:
            training_corpus = training_corpus + cur_file.read()

    train, test = train_test_split(training_corpus, test_size=0.2)

    train = "".join(train)

    unigram_probs = probability_ngram.get_unigram_prob(train, unigram_counts)

    print_json_ngram_to_file(unigram_probs, "unigram_probabilities.txt")

    bigram_probs = probability_ngram.get_bigram_prob(train, bigram_counts, unigram_counts)

    print_json_ngram_to_file(bigram_probs, "bigram_probabilities.txt")

    trigram_probs = probability_ngram.get_trigram_prob(train, trigram_counts, bigram_counts)

    print_json_ngram_to_file(trigram_probs, "trigram_probabilities.txt")


main()