import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

df = pd.read_csv("merged_dataset.csv")

df["wins_diff"] = df["t1_wins"] - df["t2_wins"]
df["map_diff_diff"] = df["t1_map_diff"] - df["t2_map_diff"]
df["round_diff_diff"] = df["t1_round_diff"] - df["t2_round_diff"]

# features we want the model to to train on
FEATURES = [
    "wins_diff",
    "map_diff_diff",
    "round_diff_diff",
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
    # ensures test matches reality, prevents misleading accuracy
    stratify=y
)

# xgboost
model = XGBClassifier(
    # num of trees, more trees -> more learning capacity
    # too few -> underfit, too many -> overfit
    n_estimators=200,
    # depth of each tree, "if else splits"
    # shallow -> generalize better, deep -> memorizes patterns
    max_depth=4,
    # essentially step sizes
    learning_rate=0.05,
    # fraction of matches used to train each tree (each only see 80% of matches, randomly sampled)
    # reduce overfitting by not letting it "memorize everything"
    subsample=0.8,
    # fraction of features used by each tree, prevent one feature from dominating
    # so not all the features of shown for all trees
    colsample_bytree=0.8,
    # defines what the task is, and the output is a probability
    objective="binary:logistic",
    # evals how wrong it is, penalizes confident wrong prediction, encourages calibrated probabilities
    eval_metric="logloss",
    random_state=42
)

#train the model
model.fit(X_train, y_train)

# predict probabilities
y_proba = model.predict_proba(X_test)[:, 1]

# convert probabilities to class labels
y_pred = (y_proba >= 0.5).astype(int)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))


