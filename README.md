This repository contains the learned demographic model and script to predict demographic proportions using the model from the paper "Demographic Dialectal Variation in Social Media: A Case Study of African-American English" by Su Lin Blodgett, Lisa Green, and Brendan O'Connor, EMNLP 2016.

The demographic model's full vocabulary and count tables (averaged over the last 50 Gibbs sampling iterations) are in `model/vocab.txt` and `model/model_count_table.txt`, respectively. Demographic predictions for a tweet can be calculated by loading the model with 

`predict.load_model(modelfile)`

and calling

`predict.predict(tweet)`

for a given tweet. Output proportions are for the African-American, Hispanic, Asian, and White topics, respectively. The model only needs to be loaded once per session.  Note that these are not confidence values about the probability of the author's demographics. Rather, these represent an inference of the *proportion* of words in the text that come from a demographically-associated language/dialect.  As we state in the paper, we only consider the AA and White categories to be reliable and useful, and conducted linguistic validation only for those two categories.

Tokenizing for the paper was done using `code/twokenize.py` and emoji detection done with `code/emoji.py`.

Python 2.7 is assumed.

Example usage:

```
$ cd code
$ python2.7

>>> import predict

>>> predict.load_model()

>>> predict.predict(u"hello there".split())
array([0.16603718, 0.27450171, 0.22886004, 0.33060107])

>>> predict.predict(u"af af af".split())
array([8.42944382e-01, 1.32149345e-01, 1.11905398e-04, 2.47943681e-02])
```

If you use this demographic model or code, please cite the paper:
```
@inproceedings{blodgett2016demographic,
author = {Blodgett, Su Lin and Green, Lisa and O'Connor, Brendan}, 
title = {{Demographic Dialectal Variation in Social Media: A Case Study of African-American English}},
booktitle = {Proceedings of EMNLP},
year = 2016}
```

More information is available at: http://slanglab.cs.umass.edu/TwitterAAE/

Please send questions to: blodgett@cs.umass.edu and brenocon@cs.umass.edu
