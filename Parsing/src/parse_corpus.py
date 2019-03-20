import subprocess
import utils
import re
from collections import Counter


def main():
    # TODO: Look for complicated sentences (with ambiguous usage of words) through the corpus and they will probably be in the wrong half of the tree
    # TODO: Also, try to find interjections like "Uhhh" they will probably be tagged incorrectly
    # TODO: Search for prepositions that are not that

    # uncomment to regenerate parsed_corpus
    for file in utils.corpus_files:
        output_file = open(utils.parsed_corpus_path + file, "w")
        subprocess.call([utils.stanford_script, utils.corpus_path + file], stdout=output_file)
        output_file.close()

    sentence_pattern = r"[(]ROOT[\n]"
    # verbs are represented by (VB|VBD|VBG|VBN|VBP|VBZ)
    verb_pattern = r"[(](VB|VBD|VBG|VBN|VBP|VBZ)\s"
    preposition_pattern = r"[(]IN\s.*[)]"

    num_sentences = 0
    num_verbs = 0
    preposition_counter = Counter(dict())
    for file in utils.parsed_corpus_files:
        cur_prepositions = Counter(dict())
        f = open(utils.parsed_corpus_path + file)
        file_preposition = open(utils.parsed_corpus_prep_count_path + file, 'w+')
        str_file = f.read()
        num_sentences += len(re.findall(sentence_pattern, str_file))
        num_verbs += len(re.findall(verb_pattern, str_file))
        prepositions = re.findall(preposition_pattern, str_file)
        for p in prepositions:
            utils.increment_dict(p, preposition_counter, 1)
            utils.increment_dict(p, cur_prepositions, 1)
        file_preposition.write(str(cur_prepositions))
        file_preposition.close()
        f.close()

    num_preposition = sum(preposition_counter.values())
    print('1.1 avg verbs: ' + str(num_verbs / num_sentences))
    print('1.2 num sentences: ' + str(num_sentences))
    print('1.3 num prepositions: ' + str(num_preposition))

    most_common_prep = preposition_counter.most_common(5)
    print('preposition #1: ' + str(most_common_prep[0][0]) + ' count: ' + str(most_common_prep[0][1]))
    print('preposition #2: ' + str(most_common_prep[1][0]) + ' count: ' + str(most_common_prep[1][1]))
    print('preposition #3: ' + str(most_common_prep[2][0]) + ' count: ' + str(most_common_prep[2][1]))
    print('preposition #4: ' + str(most_common_prep[3][0]) + ' count: ' + str(most_common_prep[3][1]))
    print('preposition #5: ' + str(most_common_prep[4][0]) + ' count: ' + str(most_common_prep[4][1]))


main()
