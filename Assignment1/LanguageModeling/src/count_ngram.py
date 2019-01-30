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

def main():
    training_set_path = os.getcwd() + '/gutenberg/'
    file_names = os.listdir(training_set_path)

    bigram = Counter({})
    for filename in file_names:
        f = open(training_set_path + filename)
        bigram += count_bigram(f.read().strip())
        f.close()

    print bigram


main()
