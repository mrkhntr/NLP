from collections import Counter
import math
import count_ngram
import utils
import os

# According to ngram_counts/unigram_counts.txt
test_set_path = os.getcwd() + '/test_data/'
test_files = os.listdir(test_set_path)
perplexity_output_path = os.getcwd() + '/perplexities/'


def perplexity(text, trigram, unigram):
    probability_sum = 0
    n = len(text)
    for c in range(0, n):
        if c + 2 < n:
            trigram_char = utils.translate_to_unk(text[c], unigram) \
                           + utils.translate_to_unk(text[c+1], unigram) \
                           + utils.translate_to_unk(text[c+2], unigram)

            if trigram.get(trigram_char) is not None:
                trigram_prob = trigram.get(trigram_char)
                probability_sum += trigram_prob

    return (-1/n) * probability_sum


def get_trigram_prob(text, trigram, bigram, λ, vocabulary_size):
    trigram_probs = {}
    for c in range(0, len(text)):
        if c + 2 < len(text):
            trigram_char = text[c] + text[c + 1] + text[c + 2]
            bigram_char = text[c] + text[c + 1]

            trigram_count = trigram.get(trigram_char)
            bigram_count = bigram.get(bigram_char)

            cur_prob = math.log((trigram_count + λ) / float(bigram_count + vocabulary_size))

            if trigram_char in trigram_probs:
                prev_prob = trigram_probs.get(trigram_char)
                trigram_probs.update({trigram_char: prev_prob + cur_prob})
            else:
                trigram_probs.update({trigram_char: cur_prob})

    return trigram_probs


def main():
    training_corpus = utils.training_set_to_str()

    unigram_counts = Counter(training_corpus)
    vocab_size = len(unigram_counts)
    bigram_counts = count_ngram.count_bigram(training_corpus)
    trigram_counts = count_ngram.count_trigram(training_corpus)
    trigram_probs = get_trigram_prob(training_corpus,
                                     trigram_counts,
                                     bigram_counts, 0.1, vocab_size)

    perplexities = open(perplexity_output_path + 'add-λ-perplexities.txt', "w")
    for filename in test_files:
        with open(test_set_path + filename, 'r', encoding='iso-8859-15') as cur_file:
            file = cur_file.read()
            score = perplexity(file, trigram_probs, unigram_counts)
            perplexities.write(filename + ", " + str(score) + "\n")
    perplexities.close()


main()
