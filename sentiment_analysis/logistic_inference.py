import pickle
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


with open('sentiment.pickle', 'rb') as f:
    clf = pickle.load(f)

with open('vectorizer.pickle', 'rb') as f:
    vectorizer = pickle.load(f)


def compute_positivity(tokens):

    sum = 0
    precision = 1

    for token in tokens:
        X_test = vectorizer.transform([token])
        y_pred_proba = clf.predict_proba(X_test)
        sum += y_pred_proba[0][1] * 100

    return round(sum / len(tokens) , precision)
