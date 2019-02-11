import utils
import os
from collections import Counter
import re


def get_tags(text):
    sentence_array = text.splitlines()

    tag_sentences = []
    for sentence in sentence_array:
        if "<s>" in sentence:
            sentence = sentence.replace("<s>", "")
            sentence = sentence.replace("</s>", "")
            word_tags = sentence.split(' ')
            new_sentence = []
            for word_tag_i in range(0, len(word_tags)):
                just_tag = re.sub(r".*\/", "", word_tags[word_tag_i])
                new_sentence.append(just_tag)
            tag_sentences.append(new_sentence)
    return tag_sentences


def add_start_end_token(filepath):
    file = utils.file_to_str(filepath)
    file = file.splitlines()

    new_file = ''
    for sentence in file:
        sentence = "<s> " + sentence + " </s>" + '\n'
        sentence = sentence.replace("<s>  </s>", "")
        sentence = sentence.replace('\t', '')

        new_file += sentence

    utils.write_to_filepath(new_file, filepath)


def count_tag_unigram(tag_sentences):
    tag_unigram = Counter({})

    for sentence in tag_sentences:
        for tag in sentence:
            utils.increment_dict(tag, tag_unigram)
    return tag_unigram


def count_tag_bigram(tag_sentences):
    tag_bigram = Counter({})

    for sentence in tag_sentences:
        for tag_i in range(0, len(sentence)):
            if tag_i + 1 != len(sentence):
                tag = sentence[tag_i] + ", " + sentence[tag_i + 1]
                utils.increment_dict(tag, tag_bigram)
    return tag_bigram


def count_word_tag(text):
    sentence_array = text.splitlines()

    word_tag_count = Counter({})
    for sentence in sentence_array:
        if "<s>" in sentence:
            word_tags = sentence.split(' ')
            for word_tag in word_tags:
                utils.increment_dict(word_tag, word_tag_count)

    word_tag_count.pop('<s>')
    word_tag_count.pop('</s>')
    return word_tag_count


def print_ngram_to_file(ngram, filename):
    file_path = utils.count_output_path + filename


    text_file = open(file_path, "w")
    text_file.write(str(ngram))
    text_file.close()


def main():
    training_files = os.listdir(utils.training_set_path)
    for filename in training_files:
        add_start_end_token(utils.training_set_path + filename)

    training_corpus = utils.training_set_to_str()
    word_tag_count = count_word_tag(training_corpus)

    tag_sentences = get_tags(training_corpus)
    tag_unigram = count_tag_unigram(tag_sentences)
    tag_bigram = count_tag_bigram(tag_sentences)

    print_ngram_to_file(word_tag_count, 'word-tag-counts.txt')
    print_ngram_to_file(tag_unigram, 'tag_unigram.txt')
    print_ngram_to_file(tag_bigram, 'tag_bigram.txt')


main()