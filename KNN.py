import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

data = pd.read_csv('dataset1.csv')

X = data.iloc[:, :-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

sns.countplot(x='Label', data=data)
plt.show()

from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=1)
model.fit(X_train, y_train)

filename = 'model.sav'
pickle.dump(model, open(filename, 'wb'))

y_pred = model.predict(X_test)

acc = metrics.accuracy_score(y_pred, y_test)
print("Accuracy is:", acc)

cm = metrics.confusion_matrix(y_pred, y_test)
print('Confusion Matrix : \n', cm)



# Classification report
classification_report = metrics.classification_report(y_pred, y_test)
print('Classification Report:\n', classification_report)

