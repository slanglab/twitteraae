This repository contains the learned demographic model and script to predict demographic proportions using the model from the paper "Demographic Dialectal Variation in Social Media: A Case Study of African-American English".

The demographic model's full vocabulary and count tables (averaged over the last 50 Gibbs sampling iterations) are in `model/vocab.txt` and `model/model_count_table.txt`, respectively. Demographic predictions for a tweet can be calculated by loading the model with 

`predict.load_model(modelfile)`

and calling

`predict.predict(tweet)`

for a given tweet. Output proportions are for the African-American, Hispanic, Asian, and White topics, respectively. The model only needs to be loaded once per session.

Tokenizing for the paper was done using `code/twokenize.py` and emoji detection done with `code/emoji.py`.

If you use this demographic model or code, please cite the paper:
```
@inproceedings{blodgett2016demographic,
author = {Blodgett, Su Lin and Green, Lisa and O'Connor, Brendan}, 
title = {{Demographic Dialectal Variation in Social Media: A Case Study of African-American English}},
booktitle = {Proceedings of EMNLP},
year = 2016}
```