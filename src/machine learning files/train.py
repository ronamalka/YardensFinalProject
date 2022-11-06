import pandas as pd
import numpy as np
import pickle

import librosa
import librosa.display

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from utils import load_data, extract_feature
from sklearn.ensemble import GradientBoostingClassifier



# load All the datasets
X_train, X_test, y_train, y_test = load_data(test_size=0.25)

model_params = {'learning_rate': 0.3,
                'max_depth': 7,
                'max_features': None,
                'min_samples_leaf': 1,
                'min_samples_split': 2,
                'n_estimators': 100,
                'subsample': 1}

model = GradientBoostingClassifier(**model_params)

# train the model
print(" Training the model...")
model.fit(X_train, y_train)

# predict 25% of data to measure how good we are
y_pred = model.predict(X_test)

# calculate the accuracy
accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)

print("Accuracy: {:.2f}%".format(accuracy * 100))

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


from sklearn.metrics import confusion_matrix
matrix = confusion_matrix(y_test, y_pred)
print(matrix)

pickle.dump(model, open("GB_classifier.model", "wb"))

