import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib

df = pd.read_csv("../data/matches_dataset.csv")

# features we want the model to to train on
FEATURES = [
    'winrate_diff',
    'form_diff',
    'rnd_diff_diff'
]

# inputting the feature
X = df[FEATURES]
# the output we want
y = df["winner"]

# train test and split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    # randomizes the split, but split is same if you use the same seed (42)
    random_state=42,
    stratify=y
)

# xgboost train
model = xgb.XGBClassifier(
    # num of trees, more trees -> more learning capacity
    # too few -> underfit, too many -> overfit
    n_estimators=100,
    # depth of each tree, "if else splits"
    # shallow -> generalize better, deep -> memorizes patterns
    max_depth=3,
    # essentially step sizes
    learning_rate=0.1,
    # evals how wrong it is, penalizes confident wrong prediction, encourages calibrated probabilities
    eval_metric="logloss",
    random_state=42
)

#train the model
model.fit(X_train, y_train)

# save
# this contains the decision trees with their split and rules
joblib.dump(model, '../model/model.pkl')

# Quick test
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.1%}")
print("Model saved as model.pkl")