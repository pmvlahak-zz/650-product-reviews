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

# def parse(filename):
#   f = gzip.open(filename, 'r')
#   entry = {}
#   for l in f:
#     l = l.strip()
#     colonPos = l.find(':')
#     if colonPos == -1:
#       yield entry
#       entry = {}
#       continue
#     eName = l[:colonPos]
#     rest = l[colonPos+2:]
#     entry[eName] = rest
#   yield entry

# reviews_list = []

# for e in parse("Toys_&_Games.txt.gz"):
#   reviews_list.append(simplejson.dumps(e))

# with open("toys_reviews.json", "w") as f:
# 	for review in reviews_list:
# 		f.write("%s\n" % review)
# f.close()


# python b.py train.csv unlabeled_test.csv prediction_file

train = "toys_reviews.json"
test = "toys_reviews.json"
# output = sys.argv[3]

train_file = open(train, 'rU').readlines()[:-1000]
train_labels = []
train_text = []

test_file = open(test, 'rU').readlines()[-1000:]
test_labels = []
test_text = []

print "Extracting text and labels..."
for line in train_file:
	review = json.loads(line)
	try:
		label = float(review.get('review/score'))
	except:
		print review.get('review/score')
		continue
	text = review.get('review/text')
	summary = review.get('review/summary')
	all_text = summary + ' '+text
	train_labels.append(label)
	train_text.append(all_text)

train_labels = np.array([int(x) for x in train_labels])


for line in test_file:
	review = json.loads(line)
	try:
		label = float(review.get('review/score'))
	except:
		print review.get('review/score')
		continue
	text = review.get('review/text')
	summary = review.get('review/summary')
	all_text = summary +' '+text
	test_labels.append(label)
	test_text.append(text)


print "Running through the pipline..."

# text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1,3))),
#                      ('tfidf', TfidfTransformer(use_idf=True)),
#                      ('feature_selection', SelectKBest(chi2, k=10000)),
#                      ('clf', MultinomialNB()),])

# text_clf = text_clf.fit(train_text, train_labels)

# text_clf_svm = Pipeline([('vect', CountVectorizer(ngram_range=(1,3))),
# 					 ('tfidf', TfidfTransformer(use_idf=True)),
# 					 ('clf', SGDClassifier()),])

# text_clf_svm = text_clf_svm.fit(train_text, train_labels)


text_clf_lsvc = Pipeline([('vect', CountVectorizer(ngram_range=(1,2))),
                     ('tfidf', TfidfTransformer(use_idf=True)),
                     ('clf', svm.LinearSVC()),])

text_clf_lsvc = text_clf_lsvc.fit(train_text, train_labels)
print "LSVC Classifier"
# with bigrams: Average diff: 0.121121121121

predicted = text_clf_lsvc.predict(test_text)

count = 0
total = 0

for score in predicted:
	diff = score - test_labels[count]
	count += 1
	total += diff

print "Average diff: "+str(total/len(predicted))

#Cross Validation
# X_train, X_test, y_train, y_test = cross_validation.train_test_split(train_text, train_labels, 
# 	test_size=0.4, random_state=0)
# print text_clf_svm.score(X_test, y_test)

# print "Starting Cross Validation...."

# scores = cross_validation.cross_val_score(text_clf_lsvc, train_text, train_labels, cv=3)
# print "Score: "+str(np.mean(scores))

# predicted = cross_validation.cross_val_predict(text_clf, train_text, train_labels, cv=3)
# print "Score: "+str(metrics.accuracy_score(train_labels, predicted))

#GridSearch for SVM
# svm_parameters = {
#     'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
#     'tfidf__use_idf': (True, False)
# }

# svm_parameters={
#     'vect__max_df': (0.5, 0.75, 1.0),
#     'vect__max_features': (None, 5000, 10000, 50000),
#     'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
#     'tfidf__use_idf': (True, False),
#     'tfidf__norm': ('l1', 'l2'),
#     'clf__alpha': (0.00001, 0.000001),
#     'clf__penalty': ('l2', 'elasticnet'),
#     'clf__n_iter': (10, 50, 80),
# }

# svm_gs_clf = GridSearchCV(text_clf_svm, svm_parameters, n_jobs=-1)
# svm_gs_clf = svm_gs_clf.fit(train_text[:500], train_labels[:500])
# best_parameters, score, _ = max(svm_gs_clf.grid_scores_, key=lambda x: x[1])
# for param_name in sorted(svm_parameters.keys()):
#     print("%s: %r" % (param_name, best_parameters[param_name]))
# print score

# #GridSearch Results
# clf__alpha: 1e-05
# clf__n_iter: 10
# clf__penalty: 'elasticnet'
# tfidf__norm: 'l2'
# tfidf__use_idf: False
# vect__max_df: 0.75
# vect__max_features: 5000
# vect__ngram_range: (1, 1)
# score: 0.684

# outfile = open(output, 'w')
# writer = csv.writer(outfile, delimiter=',')
# writer.writerow(["ID","Predicted_label"])
# for x in zip(id_list,predicted):
# 	writer.writerow(x)
# outfile.close()



























