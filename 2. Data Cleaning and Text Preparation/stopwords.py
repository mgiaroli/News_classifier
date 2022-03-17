#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stopwords
"""

import spacy

#We load spanish stopwords from https://countwordsfree.com/stopwords/spanish
my_file = open("stop_words_spanish.txt", "r")
stopwords = my_file.read()
stopwords  = stopwords.split("\n")
my_file.close()

#We use spacy for lemmatization
nlp = spacy.load('es_core_news_sm')

#we add to our stopwords the lemmatized form of them 
lemmatized_stopwords=[]        
stopwords_texto=" ".join(stopwords)
for palabra in nlp(stopwords_texto):
    lemma=palabra.lemma_
    if lemma not in stopwords and lemma not in lemmatized_stopwords:
        lemmatized_stopwords.append(lemma)
        
stopwords+=lemmatized_stopwords

with open("stopwords_spanish.txt", "w") as file:
    for word in stopwords:
        file.write("%s\n" % word)

