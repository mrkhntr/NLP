import utils
import counts
from collections import defaultdict
import re


def calc_emission_probs(word_tag_count, tag_unigram):
    d_emission = defaultdict(lambda: 1 / sum(tag_unigram.values()), {})

    vocab_size = len(tag_unigram)
    for word_tag in word_tag_count:
        word_tag_c = word_tag_count[word_tag]
        just_tag = re.sub(r".*\/", "", word_tag)
        tag_c = tag_unigram[just_tag]

        cur_prob = (word_tag_c + 1) / (float(tag_c) + vocab_size)

        utils.mult_inc_dict(word_tag, d_emission, cur_prob)

    return d_emission


def calc_transition_probs(tag_bigram, tag_unigram):
    d_transition = defaultdict(lambda: (1 / sum(tag_unigram.values())), {})
    vocab_size = len(tag_unigram)

    for bigram in tag_bigram:
        bigram_prob = tag_bigram.get(bigram)
        unigram = bigram.split(', ')[0]
        unigram_prob = tag_unigram.get(unigram)
        cur_prob = (bigram_prob + 1) / (float(unigram_prob) + vocab_size)
        utils.mult_inc_dict(bigram, d_transition, cur_prob)

    return d_transition


def main():
    training_corpus = utils.training_set_to_str()
    word_tag_count = counts.count_word_tag(training_corpus)

    tag_sentences = counts.get_tags(training_corpus)
    tag_unigram = counts.count_tag_unigram(tag_sentences)
    tag_bigram = counts.count_tag_bigram(tag_sentences)

    transition_probabilities = calc_transition_probs(tag_bigram, tag_unigram)
    emission_probabilities = calc_emission_probs(word_tag_count, tag_unigram)

    utils.print_dict_to_file(transition_probabilities,
                             utils.probabilities_path + 'transition_probabilities.txt')
    utils.print_dict_to_file(emission_probabilities,
                             utils.probabilities_path + 'emission_probabilities.txt')


main()
