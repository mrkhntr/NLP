import os
from collections import Counter
from collections import defaultdict
import utils

training_set_path = os.getcwd() + '/gutenberg/'
ngram_output_path = os.getcwd() + '/ngram_counts/'


def count_bigram(text):
    bigram_count = defaultdict(lambda: 0, {})
    for c in range(0, len(text)):
        if c+1 != len(text):
            bigram_chars = text[c] + text[c+1]

            utils.increment_dict(bigram_chars, bigram_count, 1)

    return bigram_count


assert(count_bigram('ab') == {'ab': 1})
assert(count_bigram('abc') == {'ab': 1, 'bc': 1})
assert(count_bigram('a bc') == {' b': 1, 'a ': 1, 'bc': 1})
assert(count_bigram('a bca bca bc') == {' b': 3, 'a ': 3, 'bc': 3, 'ca': 2})


def count_trigram(text):
    trigram_count = defaultdict(lambda: 0, {})
    for c in range(0, len(text)):
        if c + 2 < len(text):
            trigram_chars = text[c] + text[c + 1] + text[c + 2]

            utils.increment_dict(trigram_chars, trigram_count, 1)

    return trigram_count


assert(count_trigram('abc') == Counter({'abc': 1}))
assert(count_trigram('abcd') == Counter({'abc': 1, 'bcd': 1}))
assert(count_trigram('abcdef') == Counter({'abc': 1, 'bcd': 1, 'cde': 1, 'def': 1}))
assert(count_trigram('ab cab c') == Counter({'ab ': 2, 'b c': 2, 'cab': 1, ' ca': 1}))


def print_ngram_to_file(ngram, filename):
    file_path = ngram_output_path + filename

    text_file = open(file_path, "w")
    text_file.write(str(ngram).replace(",", ",\n"))
    text_file.close()


def main():
    training_corpus = utils.training_set_to_str()

    unigram = defaultdict(lambda: 0, (Counter(training_corpus)))
    bigram = count_bigram(training_corpus)
    trigram = count_trigram(training_corpus)

    print_ngram_to_file(dict(unigram), "unigram_counts.txt")
    print_ngram_to_file(dict(bigram), "bigram_counts.txt")
    print_ngram_to_file(dict(trigram), "trigram_counts.txt")


main()
