import probability_ngram
import count_ngram
from collections import Counter
import os
import utils
import sys

perplexity_output_path = os.getcwd() + '/perplexities/'
test_set_path = os.getcwd() + '/test_data/'
test_files = os.listdir(test_set_path)


def probability_or_zero(ngram, char):
    if ngram.get(char) is not None:
        return ngram.get(char)
    else:
        return 0


# return what unigram, bigram, trigram lambdas
# should be
def simple_grid_search(text, unigram, bigram, trigram):
    all_combos = [[0.1, 0.2, 0.7],
                  [0.1, 0.3, 0.6],
                  [0.1, 0.4, 0.5],
                  [0.1, 0.9, 0.0],
                  [0.2, 0.3, 0.5],
                  [0.2, 0.8, 0.0],
                  [0.3, 0.7, 0.0],
                  [0.4, 0.6, 0.0]]

    all_indices = [[0, 1, 2],
                   [0, 2, 1],
                   [1, 0, 2],
                   [1, 2, 0],
                   [2, 1, 0],
                   [2, 0, 1]]

    min_perplexity = sys.maxsize
    lambda_values_index = -1
    min_lambda_indices = []

    for l_i in range(0, len(all_combos)):
        for indices in all_indices:
            cur_lambda_values = all_combos[l_i]

            unigram_lambda_index = indices[0]
            bigram_lambda_index = indices[1]
            trigram_lambda_index = indices[2]

            l_tri = cur_lambda_values[trigram_lambda_index]
            l_bi = cur_lambda_values[bigram_lambda_index]
            l_uni = cur_lambda_values[unigram_lambda_index]

            cur_perplexity = interpolation_perplexity(text,
                                                      unigram, bigram, trigram,
                                                      l_tri, l_bi, l_uni)

            if cur_perplexity < min_perplexity:
                min_perplexity = cur_perplexity
                min_lambda_indices = []
                min_lambda_indices.extend([unigram_lambda_index,
                                          bigram_lambda_index,
                                          trigram_lambda_index])
                lambda_values_index = l_i

    chosen_lambda_values = all_combos[lambda_values_index]
    unigram_lambda = chosen_lambda_values[min_lambda_indices[0]]
    bigram_lambda = chosen_lambda_values[min_lambda_indices[1]]
    trigram_lambda = chosen_lambda_values[min_lambda_indices[2]]

    return unigram_lambda, bigram_lambda, trigram_lambda


def interpolation_perplexity(text, unigram, bigram, trigram, l_tri, l_bi, l_uni):
    probability_sum = 0
    n = len(text)
    for c in range(0, n):
        if c + 2 < n:
            trigram_char = text[c] + text[c+1] + text[c+2]
            bigram_char = text[c] + text[c+1]
            unigram_char = text[c]

            trigram_prob = l_tri * probability_or_zero(trigram,
                                                       trigram_char)
            bigram_prob = l_bi * probability_or_zero(bigram,
                                                     bigram_char)
            unigram_prob = l_uni * probability_or_zero(unigram,
                                                       unigram_char)

            probability_sum += (trigram_prob + bigram_prob + unigram_prob)

    return (-1/n) * probability_sum


def main():
    training_corpus = utils.training_set_to_str()

    divider = int(len(training_corpus) / 10 * 8)
    train = training_corpus[0:divider]
    held_out = training_corpus[divider:]

    unigram_counts = dict(Counter(train))
    unigram_probs = probability_ngram.get_unigram_prob(train, unigram_counts)

    bigram_counts = count_ngram.count_bigram(train)
    bigram_probs = probability_ngram.get_bigram_prob(train, bigram_counts, unigram_counts)

    trigram_counts = count_ngram.count_trigram(train)
    trigram_probs = probability_ngram.get_trigram_prob(train, trigram_counts, bigram_counts)

    unigram_lambda, bigram_lambda, trigram_lambda = simple_grid_search(held_out,
                                                                       unigram_probs,
                                                                       bigram_probs,
                                                                       trigram_probs)

    print(unigram_lambda)
    print(bigram_lambda)
    print(trigram_lambda)

    perplexities = open(perplexity_output_path + 'interpolation-perplexities.txt', "w")
    perplexities_count = {}
    for filename in test_files:
        with open(test_set_path + filename, 'r', encoding='iso-8859-15') as cur_file:
            file = cur_file.read()
            score = interpolation_perplexity(file,
                                             unigram_counts,
                                             bigram_counts,
                                             trigram_counts,
                                             trigram_lambda,
                                             bigram_lambda,
                                             unigram_lambda)
            perplexities.write(filename + ", " + str(score) + "\n")
            perplexities_count.update({filename: str(score)})
    perplexities.close()

    top_fifty = open(perplexity_output_path + 'highest-50-perplexities.txt', "w")
    top_fifty.write(str(Counter(perplexities_count).most_common(50)).replace('),', ',)\n'))
    top_fifty.close()


main()
