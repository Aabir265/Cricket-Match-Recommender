# 🏏 India Cricket Match Recommendation System

Find the **must-watch India cricket matches** based on a viewer's preferences using **Content-Based Recommendation** and **Cosine Similarity**.

This project uses historical India international cricket match data from **2001 to the present** and recommends matches based on factors such as match intensity, importance, opponent excitement, format, player presence, and recency.

---

## 📌 Project Overview

There are hundreds of India cricket matches played over the years.

Sometimes you may want to revisit an old match, but searching through hundreds of matches to find something worth watching can be difficult.

This project aims to solve that problem by building a recommendation system that understands what a viewer prefers and finds matches with similar characteristics.

For example, a viewer might prefer:

- 🔥 Intense matches
- 🏆 Important matches
- 🏏 Test / ODI / T20I
- 👤 Matches featuring specific players
- ⚔️ Matches against exciting opponents
- 🕐 Older or more recent matches

The system converts these characteristics into numerical features and uses **Cosine Similarity** to rank matches according to the user's preferences.

---

## 🚀 Features

- 📊 Historical India cricket match dataset
- 🧹 Data preparation and preprocessing
- 🧠 Feature Engineering
- 🔥 Match intensity calculation
- 🏆 Match importance calculation
- ⚔️ Opponent excitement / rivalry calculation
- 🏏 Cricket format encoding
- 👤 Player-specific features
- 🕐 Recency calculation
- 📐 Feature vector creation
- 🤖 Content-Based Recommendation
- 🔢 Cosine Similarity
- 📈 Ranking of recommended matches
- 🎯 Personalized match recommendations

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Cosine Similarity

---

## 📂 Dataset

**Dataset:** India Men's International Cricket Matches

**Source:** [Cricsheet](https://cricsheet.org/)

The dataset currently contains:

- **1,020 India men's international matches**
- **526 ODIs**
- **276 T20Is**
- **218 Tests**
- Matches spanning approximately **2001–2026**

The dataset includes information such as:

- Match ID
- Date
- Year
- Format
- Opponent
- Competition
- Match Stage
- Venue
- City
- Result
- Winning Margin
- Player of the Match
- India's Playing XI

The raw Cricsheet archive is not included in the repository because of its large file size. It can be downloaded and processed using the provided preparation script.

---

## ⚙️ Machine Learning / Recommendation Workflow

### 1. Data Preparation

Historical India international cricket match data is downloaded from Cricsheet.

The dataset is filtered to include:

- India men's matches
- International matches
- Matches from 2001 onwards
- Test, ODI and T20I formats

The processed data is stored in:

```text
data/matches.csv
2. Feature Engineering

New numerical features are created from the match data so that the recommendation system can work with the information mathematically.

Match Intensity

A match is classified as intense when the winning margin is relatively small.

Current rules:

Win by wickets → margin < 5 wickets
Win by runs    → margin < 25 runs

This produces:

1 → Intense
0 → Not Intense
Match Importance

A match is considered important when it was:

A Final
A Semi Final
Played at selected historically significant cricket venues

This produces:

1 → Important
0 → Not Important
Opponent Excitement / Rivalry

Opponent excitement is derived from the historical data rather than manually assigning arbitrary values.

The system calculates the percentage of matches against each opponent that were classified as intense.

For example:

Opponent        Intense Match Rate

Australia       ...
England         ...
Pakistan        ...
South Africa    ...

Opponents with fewer than 10 matches are excluded from the calculation to reduce the effect of very small sample sizes.

Match Format

The match format is converted into separate numerical features.

odi_format
t20_format
test_format

Example:

Test → 0 0 1
ODI  → 1 0 0
T20I → 0 1 0

This avoids treating the formats as ordered numerical values.

Player Features

Selected Indian players are represented using binary features based on whether they were part of India's playing XI.

Current player features include:

Sachin Tendulkar
Rahul Dravid
Virender Sehwag
MS Dhoni
Virat Kohli
Rohit Sharma
Jasprit Bumrah
Harbhajan Singh

Example:

1 → Player played
0 → Player did not play

This allows the recommendation system to handle preferences such as:

"I want classic India matches where Sachin played."
Recency

The match year is normalized between 0 and 1.

Older match → closer to 0
Recent match → closer to 1

This allows the recommendation system to account for a viewer's preference for older or newer cricket matches.

3. Feature Matrix

After feature engineering, the selected features are combined into a feature matrix.

The current feature matrix contains:

1,020 matches × 15 features

Current features include:

intense
importance
rivalry

odi_format
t20_format
test_format

kohli
dhoni
rohit
sachin
dravid
sehwag
bumrah
harbhajan

recency
4. User Preference Vector

A user's preferences are represented using the same features as the match vectors.

Example:

user_preferences = {
    "intense": 1,
    "importance": 0,
    "rivalry": 1,
    "odi_format": 0,
    "t20_format": 0,
    "test_format": 1,
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

The dictionary is converted into a numerical user vector using the same feature order as the match feature matrix.

5. Cosine Similarity

The recommendation system uses Cosine Similarity to compare the user's preference vector with every match vector.

Conceptually:

User Preferences
       ↓
User Feature Vector
       ↓
Cosine Similarity
       ↓
Compare with 1,020 Match Vectors
       ↓
Similarity Scores
       ↓
Sort Scores
       ↓
Recommended Matches

A higher similarity score means that the match is more aligned with the user's selected preferences.

6. Recommendation

The similarity scores are added to the dataset and the matches are sorted in descending order.

Example:

Match                         Similarity

India vs Australia (2004)       0.766
India vs Australia (2010)       0.693
India vs England (2011)        0.690
India vs Sri Lanka (2009)      0.687
India vs Australia (2003)      0.653

The highest-scoring matches become the recommendations.

🧪 Example Recommendation

A test preference profile was created around:

Intense       → Yes
Test cricket  → Yes
Sachin        → Yes
Dravid        → Yes
Harbhajan     → Yes
Classic era   → Preferred

One of the highest-ranked recommendations was:

India vs Australia
3 November 2004
Test
Wankhede Stadium

The match received a similarity score of approximately:

0.766

The recommendation was relevant to the selected preferences because:

It was a Test match
It was classified as intense
Sachin Tendulkar played
Rahul Dravid played
Virender Sehwag played
It was from the classic era

This served as an early validation of the recommendation logic.

📊 Recommendation Approach

This project currently uses Content-Based Filtering.

The system does not rely on historical user ratings or collaborative filtering.

Instead, it recommends matches based on the similarity between:

User Preferences
        ↕
Match Characteristics

This approach is suitable for the initial version because there is not yet enough user interaction data to build a collaborative filtering system.

📁 Project Structure
cricket-highlights-recommender/
│
├── main.py
├── download_and_prepare.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── matches.csv

The raw Cricsheet archive is kept locally and excluded from GitHub because of its large size.

▶️ How to Run
Clone the repository
git clone https://github.com/Aabir265/Cricket-Match-Recommender.git
Move into the project directory
cd Cricket-Match-Recommender
Install dependencies
pip install -r requirements.txt
Prepare the dataset
python download_and_prepare.py
Run the recommendation system
python main.py
🔮 Future Improvements
Build an interactive user preference interface
Allow users to select favourite players
Allow users to select preferred cricket format
Add an era / classic cricket preference
Improve the opponent excitement calculation
Add more match-specific features
Include batting and bowling performances
Detect close chases
Detect memorable finishes
Identify Super Overs and dramatic endings
Add available match highlights links
Build an interactive web application
Improve recommendation explanations
Introduce feature weighting
Collect real user feedback
Experiment with hybrid recommendation systems
Explore collaborative filtering once sufficient user interaction data is available
🧠 What I Learned

Through this project, I gained practical experience with:

Data collection and preparation
Pandas DataFrames
Data preprocessing
Feature Engineering
Creating numerical features from raw data
Working with categorical data
One-hot style encoding
Building feature vectors
Content-Based Recommendation
Cosine Similarity
Ranking recommendations
Handling missing values
Thinking about recommendation quality and user preferences
Building an end-to-end recommendation workflow using Python and Scikit-learn

One of the most valuable parts of the project was learning Feature Engineering for the first time and designing the features based on the characteristics of the actual cricket dataset rather than simply applying a pre-built model.

📌 Current Status

Work in Progress 🚧

The current version successfully performs:

✓ Data collection
✓ Data preparation
✓ Feature Engineering
✓ Feature matrix creation
✓ User preference vector creation
✓ Cosine Similarity
✓ Match ranking
✓ Basic personalized recommendations

The next stage is to improve the recommendation logic and make the system interactive so users can choose their preferred:

Era
Format
Players
Intensity
Opponents

and receive a personalized list of India cricket matches worth watching.

📜 License

This project is intended for educational, experimental, and portfolio purposes.

👨‍💻 Author

Aabir Sharma

Computer Engineering Student | AI & Machine Learning Enthusiast
