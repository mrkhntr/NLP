import utils
import os
import counts
import transition_probability
import random
import re
import sys


def generate_sentence(trans_probs, emission_probs):
    sent = ''
    first_tag = '<s>'
    generating_sentence = True
    prob = 0
    while generating_sentence:
        # First get transition.
        tags = utils.dict_items_with_substring(first_tag + ",", trans_probs)
        fst_snd_tag = random.choice(list(tags.keys()))
        prob += trans_probs[fst_snd_tag]
        second_tag = re.sub(r".*, ", "", fst_snd_tag)

        # TODO: Fix this
        if second_tag == '<e>':
            break

        # Get most likely word for second tag
        try:
            cur_words = utils.dict_items_with_substring('/' + second_tag, emission_probs)
            next_word = utils.max_value_key(cur_words)
            prob += emission_probs[next_word]
            next_word = re.sub(r"\/.*", "", next_word)
        except Exception as e:
            print('first_tag: ' + first_tag)
            print('second_tag: ' + second_tag)
            print('/second_tag: ' + '/' + second_tag)
            sys.exit()



        first_tag = second_tag
        sent += next_word + ' '
    # sent += ' <e>'
    return sent, prob


def gen_sentences():
    training_corpus = utils.training_set_to_str()
    word_tag_count = counts.count_word_tag(training_corpus)

    tag_sentences = counts.get_tags(training_corpus)
    tag_unigram = counts.count_tag_unigram(tag_sentences)
    tag_bigram = counts.count_tag_bigram(tag_sentences)

    trans_probs = transition_probability.calc_transition_probs(tag_sentences,
                                                               tag_bigram,
                                                               tag_unigram)

    emission_probs = transition_probability.calc_emission_probs(training_corpus,
                                                                word_tag_count,
                                                                tag_unigram)

    sentences = ''
    for sent in range(0, 5):
        sentence, prob = generate_sentence(trans_probs, emission_probs)
        sentences += sentence + '\n'
        sentences += str(prob) + '\n\n'

    utils.write_to_filepath(sentences, os.getcwd() + '/generated_sentences.txt')


gen_sentences()