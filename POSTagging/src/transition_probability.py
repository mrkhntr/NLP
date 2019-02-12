import utils
import counts
from collections import Counter
import math
import re
import os


def calculate_emission_probabilities(training_corpus, word_tag_count, tag_unigram):
    sentence_array = training_corpus.splitlines()

    emission_probabilities = Counter({})
    for sentence in sentence_array:
        if "<s>" in sentence:
            word_tags = sentence.replace('<s> ', '').replace(' </s>', '').split(' ')
            for word_tag in word_tags:
                word_tag_c = word_tag_count[word_tag]

                just_tag = re.sub(r".*\/", "", word_tag)
                tag_c = tag_unigram[just_tag]

                cur_prob = math.log(word_tag_c / float(tag_c))

                utils.increment_dict(word_tag, emission_probabilities, cur_prob)

    return emission_probabilities


def calculate_transition_probabilities(tag_sentences, tag_bigram, tag_unigram):
    bigram_probs = Counter({})

    for sentence in tag_sentences:
        for tag_i in range(0, len(sentence)):
            if tag_i + 1 != len(sentence):
                unigram_tag = sentence[tag_i]
                bigram_tag = sentence[tag_i] + ", " + sentence[tag_i + 1]

                bigram_prob = tag_bigram[bigram_tag]
                unigram_prob = tag_unigram[unigram_tag]

                cur_prob = math.log(bigram_prob / float(unigram_prob))

                utils.increment_dict(bigram_tag, bigram_probs, cur_prob)

    return bigram_probs


def main():
    training_corpus = utils.training_set_to_str()
    word_tag_count = counts.count_word_tag(training_corpus)

    tag_sentences = counts.get_tags(training_corpus)
    tag_unigram = counts.count_tag_unigram(tag_sentences)
    tag_bigram = counts.count_tag_bigram(tag_sentences)

    transition_probabilities = calculate_transition_probabilities(tag_sentences, tag_bigram, tag_unigram)
    emission_probabilities = calculate_emission_probabilities(training_corpus, word_tag_count, tag_unigram)

    probabilities_path = os.getcwd() + '/all_probabilities/'

    utils.print_dict_to_file(transition_probabilities,
                             probabilities_path + 'transition_probabilities.txt')
    utils.print_dict_to_file(emission_probabilities,
                             probabilities_path + 'emission_probabilities.txt')


main()