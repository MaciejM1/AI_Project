import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as pltimg
import numpy as np
import pydotplus as pydotplus
from sklearn.tree import export_graphviz, export_text
from sklearn.tree import DecisionTreeClassifier

def binDecision(params, dtree):
    result = dtree.predict([params])
    if result[0] == 0:
        return False
    else:
        return True

col_names = ['isBio', 'isFreeSpace', 'isEnough', 'isLongTime', 'isQuality', 'isPaid', 'isWinter', 'isBag', 'result']
dataset = pd.read_csv('decisionTree/params.csv')
feature_cols = ['isBio', 'isFreeSpace', 'isEnough', 'isLongTime', 'isQuality', 'isPaid', 'isWinter', 'isBag']
X = dataset[feature_cols]
X = X.values
other_cols = ['result']
y = dataset[other_cols]

dtree = DecisionTreeClassifier()
dtree.fit(X, y)
text_representation = export_text(dtree, feature_names=feature_cols)
print("[DECISION_TREE]: Struktura drzewa decyzyjnego: ")
print(text_representation)
# data = export_graphviz(dtree, out_file=None, feature_names=feature_cols)
# graph = pydotplus.graph_from_dot_data(data)
# graph.write_png('mydecisiontree.png')
#
# img = pltimg.imread('mydecisiontree.png')
# imgplot = plt.imshow(img)
# plt.show()