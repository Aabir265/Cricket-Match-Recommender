import pandas as pd
import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity , cosine_distances

# Feature Engineering to gain insights into the matches and their intensity
matches = pd.read_csv('data/matches.csv')
for i in range(len(matches)):
    if matches.loc[i, "margin_type"] == "wickets":
        intense = matches.loc[i, "margin"] < 5
    elif matches.loc[i, "margin_type"] == "runs":
        intense = matches.loc[i, "margin"] < 25
    else:
        intense = False

    if matches.loc[i, "stage"] in ["Final", "Semi Final"]:
        importance = True
    elif matches.loc[i, "venue"] in [
        "Lord's",
        "Wankhede",
        "Melbourne Cricket Ground",
        "Dubai International Cricket Stadium",
        "M. Chinnaswamy Stadium, Bengaluru",
        "Eden Gardens",
        "Kennington Oval, London",
        "Brisbane Cricket Ground",
        "Kensington Oval, Bridgetown, Barbados"

    ]:
        importance = True
    else:
        importance = False

    matches.loc[i, "intense"] = int(intense)
    matches.loc[i, "importance"] = int(importance)

rivalry = (
    matches.groupby("opponent")["intense"]
    .agg(["count", "mean"])
    .query("count >= 10")["mean"]
    .round(4)
    .sort_values(ascending=False)
)
matches["rivalry"] = matches["opponent"].map(rivalry)

matches["odi_format"] = matches["format"].apply(lambda x: 1 if x == "ODI" else 0).astype(int)
matches["t20_format"] = matches["format"].apply(lambda x: 1 if x == "T20" else 0).astype(int)
matches["test_format"] = matches["format"].apply(lambda x: 1 if x == "Test" else 0).astype(int)

min_year = matches["year"].min()
max_year = matches["year"].max()

matches["recency"] = (
    (matches["year"] - min_year)
    / (max_year - min_year)
)

matches["kohli"] = matches["india_players"].apply(lambda x: 1 if "V Kohli" in x else 0).astype(int)
matches["dhoni"] = matches["india_players"].apply(lambda x: 1 if "MS Dhoni" in x else 0).astype(int)
matches["rohit"] = matches["india_players"].apply(lambda x: 1 if "RG Sharma" in x else 0).astype(int)
matches["sachin"] = matches["india_players"].apply(lambda x: 1 if "SR Tendulkar" in x else 0).astype(int)
matches["dravid"] = matches["india_players"].apply(lambda x: 1 if "R Dravid" in x else 0).astype(int)
matches["sehwag"] = matches["india_players"].apply(lambda x: 1 if "V Sehwag" in x else 0).astype(int)
matches["bumrah"] = matches["india_players"].apply(lambda x: 1 if "JJ Bumrah" in x else 0).astype(int)
matches["harbhajan"] = matches["india_players"].apply(lambda x: 1 if "Harbhajan Singh" in x else 0).astype(int)


# Feature Matrix
feature_columns = [
    "intense",
    "importance",
    "rivalry",
    "odi_format",
    "t20_format",
    "test_format",
    "kohli",
    "dhoni",
    "rohit",
    "sachin",
    "dravid",
    "sehwag",
    "bumrah",
    "harbhajan",
    "recency"
]
X = matches[feature_columns].fillna(0)
# Compute the cosine similarity between matches based on the feature matrix
user_preferences = {
    "intense": 1,
    "importance": 1,
    "rivalry": 1,
    "odi_format": 1,
    "t20_format": 0,
    "test_format": 0,
    "kohli": 0,
    "dhoni": 0,
    "rohit": 0,
    "sachin": 1,
    "dravid": 1,
    "sehwag": 0,
    "bumrah": 0,
    "harbhajan": 1,
    "recency": 0
}
user_vector = np.array([user_preferences[col] for col in feature_columns]).reshape(1, -1)
similarites = cosine_similarity(X, user_vector).flatten()

matches["similarity"] = similarites
top_5 = matches.sort_values(
    "similarity",
    ascending=False
).head(5)

print(
    top_5[
        [
            "date",
            "opponent",
            "format",
            "stage",
            "year",
            "intense",
            "importance",
            "rivalry",
            "sachin",
            "dravid",
            "rohit",
            "sehwag",
            "harbhajan",
            "similarity"
        ]
    ].to_string(index=False)
)


