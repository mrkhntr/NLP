import math
import sys

def get_unigram_prob(text, unigram):
    unigram_probs = {}
    unigram_sum = float(sum(unigram.values()))

    for c in range(0, len(text)):
        if c + 1 != len(text):
            unigram_char = ''
            unigram_char += text[c]

            unigram_count = unigram.get(unigram_char)

            try:
                cur_prob = unigram_count / unigram_sum
            except Exception as e:
                cur_prob = sys.float_info.min

            if unigram_char in unigram_probs.keys():
                unigram_probs[unigram_char] += math.log(cur_prob)
            else:
                unigram_probs[unigram_char] = math.log(cur_prob)

    return unigram_probs

def get_bigram_prob(text, bigram, unigram):
    bigram_probs = {}
    for c in range(0, len(text)):
        if c + 1 != len(text):
            unigram_char = ''
            unigram_char += text[c]

            bigram_char = ''
            bigram_char += text[c] + text[c + 1]

            unigram_count = unigram.get(unigram_char)
            bigram_count = bigram.get(bigram_char)

            try:
                cur_prob = math.log(bigram_count / float(unigram_count))
            except Exception as e:
                cur_prob = sys.float_info.min

            if bigram_char in bigram_probs.keys():
                bigram_probs[bigram_char] += cur_prob
            else:
                bigram_probs[bigram_char] = cur_prob

    return bigram_probs


def get_trigram_prob(text, trigram, bigram):
    trigram_probs = {}
    for c in range(0, len(text)):
        if c + 2 < len(text):
            trigram_char = ''
            trigram_char += text[c] + text[c + 1] + text[c + 2]

            bigram_char = ''
            bigram_char += text[c] + text[c + 1]

            trigram_count = trigram.get(trigram_char)
            bigram_count = bigram.get(bigram_char)

            try:
                cur_prob = math.log(trigram_count / float(bigram_count))
            except Exception as e:
                cur_prob = sys.float_info.min

            if trigram_char in trigram_probs.keys():
                trigram_probs[trigram_char] += cur_prob
            else:
                trigram_probs[trigram_char] = cur_prob

    return trigram_probs
