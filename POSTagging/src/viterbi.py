import utils
import counts
import calculate_probabilities
import re
import sys
from collections import defaultdict


# the sentence this function receives will only be the words + punc
# THIS MEANS NO sentence_id and no <EOS>
def viterbi(sentence, trans_probs, emission_probs, tag_unigram):
    sentence_array = sentence.splitlines()

    π = []  # Represented by [ { all_possible_tags }, { apt }2, { apt }3, ... {apt}n] n = len(sentence)
    bp = []  # Represented by [ { state_1: start, state_2: start...},
    #    { state_1: max_prev_state, state_2: max_prev_state...}
    #    ... ]

    initial_word = sentence[0]
    init_state_probs = defaultdict(lambda: 1 / sum(tag_unigram.values()))
    init_bps = {}
    for state in tag_unigram.keys():
        cur_prob = tag_unigram[state] * emission_probs[initial_word + '/' + state]
        utils.increment_dict(state, init_state_probs, cur_prob)
        init_bps.update({state: '<START>'})

    π.append(init_state_probs)
    bp.append(init_bps)

    for word_i in range(1, len(sentence_array)):
        all_state_probs = defaultdict(lambda: 1 / sum(tag_unigram.values()))
        cur_bp_states = {}
        π.append(all_state_probs)
        bp.append(cur_bp_states)

        for possible_next_state in tag_unigram.keys():
            max_state_prob = -sys.maxsize - 1
            max_state_prime = None

            for state_prime in tag_unigram.keys():
                pos_prev_state = π[word_i - 1][state_prime]
                trans_prob = trans_probs[state_prime + ', ' + possible_next_state]
                emission_prob = emission_probs[sentence_array[word_i] + '/' + possible_next_state]

                cur_state_prob = pos_prev_state * trans_prob * emission_prob

                if cur_state_prob > max_state_prob:
                    max_state_prob = cur_state_prob
                    max_state_prime = state_prime

            utils.increment_dict(max_state_prime, all_state_probs, max_state_prob)
            cur_max_state = utils.max_value_key(all_state_probs)
            cur_bp_states.update({possible_next_state: cur_max_state})

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
    test_file_sentences.pop(125)  # Last sentence is empty

    output = ''
    for sentence in test_file_sentences:
        sentence_tag = sentence.lstrip().split('\n')[0]
        sentence = re.sub(r"" + sentence_tag + '\n', "", sentence).lstrip()
        best_path, best_path_prob = viterbi(sentence, trans_probs, emission_probs, tag_unigram)
        output += sentence_tag + '\n'
        for i in range(0, len(best_path)):
            output += sentence[i] + ', ' + best_path[i]
        output += '<EOS>\n'

    utils.write_to_filepath(output, 'Test_File_Solution.txt')


main()
