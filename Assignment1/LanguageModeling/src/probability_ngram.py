import math
import self as self

# NOTE: The unigram and bigram models in the tests
# do not necessarily model the text exactly

# TODO: 1) Should we worry about not being able to find a character
#   in our dict, and returning some minimum probability?
#   2) Test error case for unigram prob
def unigram_prob(text, index, unigram):
    if index < len(text) and index >= 0:
        unigram_char = text[index]
        unigram_count = unigram.get(unigram_char)

        unigram_prob = unigram_count / float(sum(unigram.values()))
        return math.log(unigram_prob)
    else:
        raise IndexError('This index does not exist in the text')


assert(unigram_prob('abc', 0, {'a': 1, 'b': 1, 'c': 1}) == -1.0986122886681098)


def bigram_prob(text, index, bigram, unigram):
    if index+1 != len(text):
        unigram_char = text[index]
        bigram_char = text[index] + text[index+1]

        unigram_count = unigram.get(unigram_char)
        bigram_count = bigram.get(bigram_char)

        cur_prob = bigram_count / float(unigram_count)

        return math.log(cur_prob)
    else:
        return unigram_prob(text, index, unigram)


assert(bigram_prob('abc', 0, {'ab': 1, 'bc': 1},
                             {'a': 2, 'b': 2, 'c': 2}) == -0.6931471805599453)
assert(bigram_prob('abc', 1, {'ab': 1, 'bc': 1},
                             {'a': 2, 'b': 2, 'c': 2}) == -0.6931471805599453)
assert(bigram_prob('abc', 2, {'ab': 1, 'bc': 1},
                             {'a': 2, 'b': 2, 'c': 2}) == -1.0986122886681098)
assert(bigram_prob('ab?', 2, {'ab': 1, 'bc': 1, 'b?': 1},
                             {'a': 2, 'b': 2, 'c': 2, '?': 3}) == -1.0986122886681098)
assert(bigram_prob('ab?c', 2, {'ab': 1, 'bc': 1, '?c': 1},
                              {'a': 2, 'b': 2, 'c': 2, '?': 3}) == -1.0986122886681098)


def trigram_prob(text, index, trigram, bigram, unigram):
    if index + 2 < len(text):
        bigram_char = text[index] + text[index + 1]
        trigram_char = text[index] + text[index + 1] + text[index + 2]

        bigram_count = bigram.get(bigram_char)
        trigram_count = trigram.get(trigram_char)

        cur_prob = trigram_count / float(bigram_count)
        return math.log(cur_prob)
    else:
        return bigram_prob(text, index, bigram, unigram)


assert(trigram_prob('abc', 2, {'abc': 1},
                              {'ab': 1, 'bc': 1},
                              {'a': 2, 'b': 2, 'c': 2}) == -1.0986122886681098)

assert(trigram_prob('abcdef', 2, {'abc': 1, 'bcd': 1, 'cde': 1, 'def': 1},
                                 {'ab': 1, 'bc': 1, 'cd': 3},
                                 {'a': 2, 'b': 2, 'c': 2}) == -1.0986122886681098)
