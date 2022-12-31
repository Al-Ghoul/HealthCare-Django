from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import numpy as np
import pandas as pd
import re
import csv

training = pd.read_csv('main/Data/Training.csv')
testing = pd.read_csv('main/Data/Testing.csv')
cols = training.columns
cols = cols[:-1]
x = training[cols]
y = training['prognosis']
y1 = y


reduced_data = training.groupby(training['prognosis']).max()

# mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.33, random_state=42)
testx = testing[cols]
testy = testing['prognosis']
testy = le.transform(testy)


clf1 = DecisionTreeClassifier()
clf = clf1.fit(x_train, y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
scores = cross_val_score(clf, x_test, y_test, cv=3)
# print (scores)
print(scores.mean())


model = SVC()
model.fit(x_train, y_train)
print("for svm: ")
print(model.score(x_test, y_test))

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols


def check_pattern(dis_list, inp):
    pred_list = []
    inp = inp.replace(' ', '_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list = [item for item in dis_list if regexp.search(item)]
    if (len(pred_list) > 0):
        return 1, pred_list
    else:
        return 0, []


severityDictionary = dict()
description_list = dict()
precautionDictionary = dict()

symptoms_dict = {}
for index, symptom in enumerate(x):
    symptoms_dict[symptom] = index

def getDescription():
    global description_list
    with open('main/MasterData/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)

def getSeverityDict():
    global severityDictionary
    with open('main/MasterData/symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass


def getprecautionDict():
    global precautionDictionary
    with open('main/MasterData/symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)

getSeverityDict()
getDescription()
getprecautionDict()

def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return list(map(lambda x: x.strip(), list(disease)))


def sec_predict(symptoms_exp):
    df = pd.read_csv('main/Data/Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])


def calc_condition(exp, days):
    sum = 0
    for item in exp:
        sum = sum+severityDictionary[item]
    if ((sum*days)/(len(exp)+1) > 13):
        return "You should take the consultation from doctor."
    else:
        return "It might not be that bad but you should take precautions."


def recurse(request, node=0, depth=1):
    cols = training.columns
    cols = cols[:-1]
    x = training[cols]
    y = training['prognosis']
    y1 = y

    reduced_data = training.groupby(training['prognosis']).max()

    # mapping strings to numbers
    le = preprocessing.LabelEncoder()
    le.fit(y)
    y = le.transform(y)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.33, random_state=42)
    testx = testing[cols]
    testy = testing['prognosis']
    testy = le.transform(testy)

    clf1 = DecisionTreeClassifier()
    clf = clf1.fit(x_train, y_train)


    tree_ = clf.tree_
    feature_names = cols
    symptoms_present = []
    feature_names = cols
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        threshold = tree_.threshold[node]

        if name == request.session['symp']:
            val = 1
        else:
            val = 0
        if val <= threshold:
            recurse(request, tree_.children_left[node], depth + 1)
        else:
            symptoms_present.append(name)
            recurse(request, tree_.children_right[node], depth + 1)
    else:
        present_disease = print_disease(tree_.value[node])
        red_cols = reduced_data.columns
        symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero(
        )]

        request.session['present_disease'] = present_disease
        request.session['questions'] = []
        for sym in list(symptoms_given):
            request.session['questions'].append(sym)