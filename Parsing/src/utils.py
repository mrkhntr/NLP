import os

stanford_script = os.getcwd() + '/stanford-parser-full-2018-10-17/lexparser.sh'
corpus_path = os.getcwd() + '/corpus/'
corpus_files = os.listdir(corpus_path)
parsed_corpus_path = os.getcwd() + '/parsed_corpus/'
parsed_corpus_prep_count_path = os.getcwd() + '/parsed_corpus_preposition_count/'
parsed_corpus_files = os.listdir(parsed_corpus_path)


def increment_dict(key, dictionary, increment):
    if key not in dictionary:
        dictionary[key] = increment
    else:
        dictionary[key] += increment
