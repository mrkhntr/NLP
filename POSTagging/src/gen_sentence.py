import utils
import os


def generate_sentence():


def gen_sentences():
    sentences = ''
    for sent in range(0, 6):
        sentences += '<s> ' + generate_sentence() + ' <e>\n'

    utils.write_to_filepath(sentences, os.getcwd() + '/generated_sentences.txt')


gen_sentences()