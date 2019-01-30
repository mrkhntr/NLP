import os
from collections import Counter

def count_bigram(text):
    bigram_count = Counter({})
    for c in range(0, len(text)):
        if c+1 != len(text):
            entry = ''
            entry += text[c] + text[c+1]

            if entry in bigram_count:
                bigram_count[entry] += 1
            else:
                bigram_count[entry] = 1

    print bigram_count
    return bigram_count

assert(count_bigram('ab') == Counter({'ab': 1}))
assert(count_bigram('abc') == Counter({'ab': 1, 'bc': 1}))
assert(count_bigram('a bc') == Counter({' b': 1, 'a ': 1, 'bc': 1}))
assert(count_bigram('a bca bca bc') == Counter({' b': 3, 'a ': 3, 'bc': 3, 'ca': 2}))

def count_trigram(text):
    trigram_count = Counter({})
    for c in range(0, len(text)):
        if c + 2 < len(text):
            entry = ''
            entry += text[c] + text[c + 1] + text[c + 2]
            if entry in trigram_count:
                trigram_count[entry] += 1
            else:
                trigram_count[entry] = 1

    print trigram_count
    return trigram_count

assert(count_trigram('abc') == Counter({'abc': 1}))
assert(count_trigram('abcd') == Counter({'abc': 1, 'bcd': 1}))
assert(count_trigram('abcdef') == Counter({'abc': 1, 'bcd': 1, 'cde': 1, 'def': 1}))
assert(count_trigram('ab cab c') == Counter({'ab ': 2, 'b c': 2, 'cab': 1, ' ca': 1}))

def main():
    training_set_path = os.getcwd() + '/gutenberg/'
    file_names = os.listdir(training_set_path)

    trigram = Counter({})
    for filename in file_names:
        f = open(training_set_path + filename)
        trigram += count_trigram(f.read().strip())
        f.close()

    print trigram


# main()
