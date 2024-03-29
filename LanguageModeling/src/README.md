### Language Model

#### Unigram, Bigram, Trigram Counts
 
* These counts are located in the ngram_counts folder
* They can be regenerated by :
1) Unzipping a gutenberg.zip 
file and removing the README.md
2) Running data_preprocess.py
3) Running count_ngram.py

#### Simple Interpolation Language Model

* Disclaimer: This model will take a while
to run.
* Prerequisites:
    1) Requires test_data to be unzipped in the 
    src folder.
    2) Requires a perplexities folder to output
    results to.
    3) Requires a gutenberg.zip to be unzipped,
    with README removed, and data_preprocess ran.
    
Running simple_interpolation.py alone will output
the best lambda values determined by simple interpolation
to the console. 0.0 for the unigram lambda, 0.1 for the bigram 
lambda, and 0.9 for the trigram lambda. It will also 
output interpolation-perplexities.txt and highest-50-perplexities.txt.


#####Note: If one uses unigram, bigram, trigram counts instead of probabilities, the highest perplexity files are all french
#####Note: The original submitted highest-50-perplexities.txt contains whether or not they are French.

#### Add-λ Smoothing Language Model

This model just needs the training set to be data_preprocess'd.
The test_data needs to be unzipped.
Running the add-λ-lm.py alone should give all perplexities.
 