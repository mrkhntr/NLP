import os
from collections import Counter
import fileinput

training_set_path = os.getcwd() + '/gutenberg/'
ngram_output_path = os.getcwd() + '/ngram_counts/'


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

    return trigram_count


assert(count_trigram('abc') == Counter({'abc': 1}))
assert(count_trigram('abcd') == Counter({'abc': 1, 'bcd': 1}))
assert(count_trigram('abcdef') == Counter({'abc': 1, 'bcd': 1, 'cde': 1, 'def': 1}))
assert(count_trigram('ab cab c') == Counter({'ab ': 2, 'b c': 2, 'cab': 1, ' ca': 1}))


def count_ngrams(ngram_method):
    ngram = Counter({})
    training_set_path = os.getcwd() + '/gutenberg/'
    file_names = os.listdir(training_set_path)

    for filename in file_names:
        f = open(training_set_path + filename)
        ngram += ngram_method(f.read().strip())
        f.close()

    return ngram


def print_json_ngram_to_file(ngram, filename):
    file_path = ngram_output_path + filename

    text_file = open(file_path, "w")
    text_file.write(str(ngram))
    text_file.close()
    jsonify_file(file_path)


def jsonify_line(line):
    # NOTE WE NEED TO REMOVE THE COUNTER FROM THE FIRST AND LAST LINE
    line = line.replace("Counter(", "")
    line = line.replace(")", "")

    line = line.replace(',', ',\n')
    line = line.replace("'", "\"")
    return line


def jsonify_file(filename):
    for line in fileinput.FileInput(filename, inplace=1):
        line = jsonify_line(line)
        print(line, end='')


def main():
    #  The Counter object by itself will just aggregate letter counts
    unigram = count_ngrams(Counter)
    bigram = count_ngrams(count_bigram)
    trigram = count_ngrams(count_trigram)

    print_json_ngram_to_file(unigram, "unigram_counts.txt")
    print_json_ngram_to_file(bigram, "bigram_counts.txt")
    print_json_ngram_to_file(trigram, "trigram_counts.txt")


main()
