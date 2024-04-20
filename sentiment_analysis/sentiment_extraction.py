import csv
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

r_n = 1

# open the CSV file
with open('train.csv', 'r', encoding='utf-8') as csvfile:
    # create a CSV reader object
    csvreader = csv.reader(csvfile)
    print('test')
    x_train = []
    y_train = []

    # iterate over each row in the CSV file
    for row in csvreader:
        r_n += 1
        print(r_n)
        if r_n == 1000000:
            break
        # iterate over each element in the row
        ite = 0
        for element in row:
            # do something with the element
            if ite == 0:
                y_train.append(int(element))
                y_train.append(int(element))
            elif ite == 1:
                x_train.append(element)
            else:
                x_train.append(element)
            ite += 1

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(x_train)

    # Train logistic regression model on the training data
    clf = LogisticRegression(max_iter=5000)
    clf.fit(X_train, y_train)


    with open('sentiment.pickle', 'wb') as f:
        pickle.dump(clf, f)

    with open('vectorizer.pickle', 'wb') as f:
        pickle.dump(vectorizer, f)

    # Example prediction
    while True:
        test_text = input()
        X_test = vectorizer.transform([test_text])
        y_pred_proba = clf.predict_proba(X_test)
        print('Positivitiy: ', y_pred_proba[0][1] * 100, '%')
