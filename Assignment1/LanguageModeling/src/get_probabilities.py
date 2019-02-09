import json
import os
import probability_ngram
import count_ngram
from sklearn.model_selection import train_test_split

training_set_path = os.getcwd() + '/gutenberg/'
file_names = os.listdir(training_set_path)
ngram_probability_path = os.getcwd() + '/ngram_probabilities/'


def print_json_ngram_to_file(ngram, filename):
    file_path = ngram_probability_path + filename

    text_file = open(file_path, "w")
    text_file.write(str(ngram))
    text_file.close()
    # count_ngram.jsonify_file(file_path)


def get_ngram_probs(train, ngram_probability, ngram_counts):
    ngram_probs = {}
    for c in range(0, len(train)):
        if c+1 != len(train):
            text_and_prob = ngram_probability(train, c, ngram_counts)
            cur_char = text_and_prob.get('text')
            new_prob = text_and_prob.get('prob')

            if cur_char in ngram_probs:
                cur_prob = ngram_probs.get(cur_char)
                ngram_probs.update({cur_char: cur_prob + new_prob})
            else:
                ngram_probs.update({cur_char: new_prob})

    return ngram_probs

def main():
    with open(os.getcwd() + '/ngram_counts/unigram_counts.txt') as fh:
        unigram_counts = json.load(fh)

    with open(os.getcwd() + '/ngram_counts/bigram_counts.txt') as fh:
        bigrams_counts = json.load(fh)

    with open(os.getcwd() + '/ngram_counts/trigram_counts.txt') as fh:
        trigrams_counts = json.load(fh)

    training_corpus = ''
    for filename in file_names:
        with open(training_set_path + filename, 'r') as cur_file:
            training_corpus = training_corpus + cur_file.read()

    train, test = train_test_split(training_corpus, test_size=0.2)

    unigram_probs = get_ngram_probs(train, probability_ngram.unigram_prob, unigram_counts)
    print_json_ngram_to_file(unigram_probs, "unigram_probabilities.txt")
    bigram_probs = get_ngram_probs(train, probability_ngram.unigram_prob, bigrams_counts)
    print_json_ngram_to_file(bigram_probs, "bigram_probabilities.txt")
    trigram_probs = get_ngram_probs(train, probability_ngram.unigram_prob, trigrams_counts)
    print_json_ngram_to_file(trigram_probs, "trigram_probabilities.txt")


main()
