#!/usr/bin/python

from __future__ import division
from sklearn.datasets import fetch_20newsgroups
from sklearn import datasets
import os, sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.grid_search import GridSearchCV
import csv
from sklearn import cross_validation
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import svm
import gzip
import json
from sklearn.externals import joblib


test_file = open("input.txt", "rU").readlines()
test_text = []

for line in test_file:
    review = json.loads(line.replace('\r\n', '\\r\\n'))
    if review.get('category') == "Electronics":
        model = "electronics.pkl"
    elif review.get('category') == "Health":
        model = "health.pkl"
    elif review.get('category') == "Food":
        model = "gourmet_foods.pkl"
    elif review.get('category') == "Clothing":
        model = "clothing.pkl"
    elif review.get('category') == "Toys & Games":
        model = "toys_and_games.pkl"
    text = review.get('text')
    summary = review.get('title')
    all_text = summary +' '+text
    all_text = text
    test_text.append(all_text)

text_clf_lsvc = joblib.load(model)
predicted = text_clf_lsvc.predict(test_text)
output = {"score": predicted[0]}
print json.dumps(output)
