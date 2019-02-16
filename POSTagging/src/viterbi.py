import utils
import counts
import calculate_probabilities
import re
import sys
from collections import defaultdict


def viterbi(sentence_array, trans_probs, emission_probs, tag_unigram):
    π = []  # Represented by [ { all_possible_tags }, { apt }2, { apt }3, ... {apt}n] n = len(sentence)

    # initialize the states in the first entry's dictionary
    initial_word = sentence_array[0]
    init_state_probs = defaultdict(lambda: 1 / sum(tag_unigram.values()))
    init_bps = {}
    for state in tag_unigram.keys():
        cur_prob = tag_unigram[state] * emission_probs[initial_word + '/' + state]
        utils.increment_dict(state, init_state_probs, cur_prob)
        init_bps.update({state: '<START>'})

    π.append(init_state_probs)

    for word_i in range(1, len(sentence_array)):
        all_state_probs = defaultdict(lambda: 1 / sum(tag_unigram.values()))
        cur_bp_states = {}
        π.append(all_state_probs)

        # for a given state that word_i would end at
        for possible_next_state in tag_unigram.keys():
            max_state_prob = -sys.maxsize - 1
            max_state_prime = None

            # for any state that word_i may have come from in the previous index
            for state_prime in tag_unigram.keys():
                pos_prev_state = π[word_i - 1][state_prime]
                # transitioning from that theoretical previous state, to this considered state
                trans_prob = trans_probs[state_prime + ', ' + possible_next_state]
                # the probability that this word belongs to this potential state
                emission_prob = emission_probs[sentence_array[word_i] + '/' + possible_next_state]

                # calculate the probability of this word, tag pairing
                cur_state_prob = pos_prev_state * trans_prob * emission_prob

                if cur_state_prob > max_state_prob:
                    max_state_prob = cur_state_prob
                    max_state_prime = state_prime

            # take the maximum state_prime to this considered state, and attach that
            # to this π[word_i][possible_next_state]
            utils.increment_dict(max_state_prime, all_state_probs, max_state_prob)

    # iterate through each word_i and get the most likely state at that word_i
    best_path = []
    best_path_prob = 1
    for word_i in range(1, len(sentence_array)):
        cur_states = π[word_i]
        best_tag = utils.max_value_key(cur_states)

        best_path_prob *= cur_states[best_tag]
        best_path.append(best_tag)

    return best_path, best_path_prob


def main():
    training_corpus = utils.training_set_to_str()
    word_tag_count = counts.count_word_tag(training_corpus)

    tag_sentences = counts.get_tags(training_corpus)
    tag_unigram = counts.count_tag_unigram(tag_sentences, include_sent_token=False)
    tag_bigram = counts.count_tag_bigram(tag_sentences, include_sent_token=False)

    trans_probs = calculate_probabilities.calc_transition_probs(tag_bigram, tag_unigram)
    emission_probs = calculate_probabilities.calc_emission_probs(word_tag_count, tag_unigram)

    test_file = utils.file_to_str(utils.test_file_path)
    test_file_sentences = test_file.split('<EOS>')
    test_file_sentences.pop(len(test_file_sentences) - 1)  # Last sentence is empty

    output = ''
    for sentence in test_file_sentences:
        sentence_tag = sentence.lstrip().split('\n')[0]
        sentence = re.sub(r"" + sentence_tag + '\n', "", sentence).lstrip()
        sentence_array = sentence.splitlines()
        best_path, best_path_prob = viterbi(sentence_array, trans_probs, emission_probs, tag_unigram)
        output += sentence_tag + '\n'
        for i in range(0, len(best_path)):
            output += sentence_array[i] + ', ' + best_path[i] + '\n'
        output += '<EOS>\n'

    # use solutions path here
    utils.write_to_filepath(output, utils.solutions_path + 'Test_File_Solution.txt')


main()
