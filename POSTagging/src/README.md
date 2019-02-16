### POS Tagging Model

#### Pre-steps
* Unzip brown_corpus_spring2019.zip
* Remove cats.txt from this directory

#### Word-Tag Counts, Tag Unigram/Bigram Counts
* Run counts.py and this should fill all_counts directory

#### Probabilities
* Run calculate_probabilities.py to fill the probabilities
* Used Add-one smoothing here
* The unk threshold was under 6

#### Generating Random Sentences
* Running gen_sentence.py alone should generate sentences under solutions/generated_sentences.txt
* Sometimes the sentences are too short, but running them a few times will make longer ones
* The probabilities also sum up to 0 at times, due to underflow

#### Viterbi
* Running the viterbi.py alone should fill solutions/Test_File_Solution.txt
* Running this may take a while
