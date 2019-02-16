import math
import os
import utils
from collections import defaultdict

training_set_path = os.getcwd() + '/gutenberg/'
file_names = os.listdir(training_set_path)
ngram_probability_path = os.getcwd() + '/ngram_probabilities/'


def print_prob_ngram_to_file(ngram, filename):
    file_path = ngram_probability_path + filename

    utils.write_to_filepath(str(ngram).replace(",", ",\n"), file_path)


def get_unigram_probs(unigram):
    unigram_sum = float(sum(unigram.values()))
    unigram_probs = defaultdict(lambda: 1/unigram_sum, {})

    for unigram_char in unigram:
        unigram_count = unigram.get(unigram_char)

        cur_prob = math.log(unigram_count / unigram_sum)

        utils.increment_dict(unigram_char, unigram_probs, cur_prob)

    return unigram_probs


def get_bigram_probs(bigram, unigram):
    bigram_probs = defaultdict(lambda: 1/(float(sum(unigram.values()))), {})
    for bigram_char in bigram:
        unigram_char = bigram_char[0]

        unigram_count = unigram.get(unigram_char)
        bigram_count = bigram.get(bigram_char)

        cur_prob = math.log(bigram_count / float(unigram_count))

        utils.increment_dict(bigram_char, bigram_probs, cur_prob)

    return bigram_probs


def get_trigram_probs(trigram, bigram, unigram):
    trigram_probs = defaultdict(lambda: 1/(float(sum(unigram.values()))), {})

    for trigram_char in trigram:
        bigram_char = trigram_char[0] + trigram_char[1]

        trigram_count = trigram.get(trigram_char)
        bigram_count = bigram.get(bigram_char)

        cur_prob = math.log(trigram_count / float(bigram_count))

        utils.increment_dict(trigram_char, trigram_probs, cur_prob)

    return trigram_probs
