import pickle
from models_parameters import classification_grid_parameters
from sklearn.metrics import accuracy_score,mean_squared_error,make_scorer
from utils import load_data, extract_feature
from sklearn.model_selection import GridSearchCV

emotions = ["neutral", "happy", "sad", "angry", "fearful"]

# load All the datasets
X_train, X_test, y_train, y_test = load_data(test_size=0.25)

best_estimators = []


for model, params in classification_grid_parameters.items():
    if model.__class__.__name__ == "KNeighborsClassifier":
        # in case of a K-Nearest neighbors algorithm
        # set number of neighbors to the length of emotions
        params['n_neighbors'] = [len(emotions)]
    score = accuracy_score
    grid = GridSearchCV(estimator=model, param_grid=params, scoring=make_scorer(score),
                        n_jobs=4, verbose=1, cv=3)
    grid_result = grid.fit(X_train, y_train)
    best_estimator = grid_result.best_estimator_
    best_params = grid_result.best_params_
    cv_best_score = grid_result.best_score_
    best_estimators.append((best_estimator, best_params, cv_best_score))
    print(
        f"{emotions} {best_estimator.__class__.__name__} achieved {cv_best_score:.3f} cross validation accuracy score!")
    print(f"the best parm : { best_params} ")



