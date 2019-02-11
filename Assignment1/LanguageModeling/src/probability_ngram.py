import math
import os
import utils

training_set_path = os.getcwd() + '/gutenberg/'
file_names = os.listdir(training_set_path)
ngram_probability_path = os.getcwd() + '/ngram_probabilities/'


def print_prob_ngram_to_file(ngram, filename):
    file_path = ngram_probability_path + filename

    utils.write_to_filepath(str(ngram).replace(",", ",\n"), file_path)


def get_unigram_prob(text, unigram):
    unigram_probs = {}
    unigram_sum = float(sum(unigram.values()))

    for c in range(0, len(text)):
        if c + 1 != len(text):
            unigram_char = text[c]

            unigram_count = unigram.get(unigram_char)

            cur_prob = math.log(unigram_count / unigram_sum)

            utils.increment_dict(unigram_char, unigram_probs, cur_prob)

    return unigram_probs


def get_bigram_prob(text, bigram, unigram):
    bigram_probs = {}
    for c in range(0, len(text)):
        if c + 1 != len(text):
            unigram_char = text[c]

            bigram_char = text[c] + text[c + 1]

            unigram_count = unigram.get(unigram_char)
            bigram_count = bigram.get(bigram_char)

            cur_prob = math.log(bigram_count / float(unigram_count))

            utils.increment_dict(bigram_char, bigram_probs, cur_prob)

    return bigram_probs


assert(get_bigram_prob('sissi',
                       {'si': 2, 'is': 1, 'ss': 1},
                       {'s': 3, 'i': 2}) == {'si': -0.8109302162163289,
                                             'is': -0.6931471805599453,
                                             'ss': -1.0986122886681098})


def get_trigram_prob(text, trigram, bigram):
    trigram_probs = {}
    for c in range(0, len(text)):
        if c + 2 < len(text):
            trigram_char = text[c] + text[c + 1] + text[c + 2]
            bigram_char = text[c] + text[c + 1]

            trigram_count = trigram.get(trigram_char)
            bigram_count = bigram.get(bigram_char)

            cur_prob = math.log(trigram_count / float(bigram_count))

            utils.increment_dict(trigram_char, trigram_probs, cur_prob)

    return trigram_probs
