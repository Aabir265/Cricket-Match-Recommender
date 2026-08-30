# 🏏 Cricket Match Recommender

A content-based recommendation system that recommends **must-watch India cricket matches** based on what a viewer is interested in.

The idea behind this project is simple:

> There are hundreds of India matches from the past. If someone wants to watch highlights but doesn't know which match to pick, why not recommend one based on what they like?

For example, a viewer might prefer:

- Intense matches
- Test cricket
- Classic Indian cricket
- Matches involving Sachin Tendulkar or Rahul Dravid
- Certain opponents
- Older or more recent matches

The system converts these preferences into numerical feature vectors and uses **cosine similarity** to find matches that are most similar to the viewer's preferences.

---

## 🎯 Project Goal

The goal is to build a recommendation system that can answer:

**"Which past India cricket matches should I watch?"**

Instead of recommending matches randomly, the system looks at different characteristics of each match and ranks them according to the user's preferences.

---

## 📊 Dataset

The current dataset contains:

- **1,020 India international matches**
- Formats:
  - Test
  - ODI
  - T20I
- Matches spanning approximately **2001–2026**
- Multiple opponents including Australia, England, Pakistan, South Africa, Sri Lanka, West Indies and others.

The raw dataset is prepared before being used by the recommendation system.

The large raw dataset is intentionally not stored in this repository.

---

## ⚙️ How It Works

The project currently follows this pipeline:

```text
Cricket Match Data
        ↓
Data Preparation
        ↓
Feature Engineering
        ↓
Feature Matrix
        ↓
User Preference Vector
        ↓
Cosine Similarity
        ↓
Similarity Scores
        ↓
Rank Matches
        ↓
Recommended Matches 🏏
🧠 Feature Engineering

Each match is represented using numerical features.

Match Intensity

A match is considered intense when the winning margin is relatively small.

Current rules:

Win by wickets → margin < 5 wickets
Win by runs    → margin < 25 runs

This produces a binary feature:

1 → Intense
0 → Not intense
Match Importance

A match receives an importance score based on whether it was:

A Final
A Semi Final
Played at selected historically significant venues

The feature is represented as:

1 → Important
0 → Not important
Opponent Excitement / Rivalry

Instead of manually assigning a rivalry score to every opponent, the current system derives it from the dataset.

The score is based on the percentage of India's matches against an opponent that were classified as intense.

For example:

Opponent → Intense Match Rate
Australia → ...
England   → ...
Pakistan  → ...

Opponents with very few matches are excluded from the calculation to avoid unreliable percentages caused by small sample sizes.

Match Format

The format is converted into numerical features:

odi_format
t20_format
test_format

For example:

Test → 0 0 1
ODI  → 1 0 0
T20I → 0 1 0

This avoids treating formats as ordered numerical values.

Player Features

The system also considers whether selected players were part of India's playing XI.

Current player features include players such as:

Sachin Tendulkar
Rahul Dravid
Virender Sehwag
MS Dhoni
Virat Kohli
Rohit Sharma
Jasprit Bumrah
Harbhajan Singh

Each player feature is represented as:

1 → Player played
0 → Player did not play

This allows the recommender to handle preferences such as:

"Show me classic India matches where Sachin played."

Recency

The match year is normalized between 0 and 1.

Older matches receive values closer to 0, while newer matches receive values closer to 1.

This allows the recommendation system to consider a viewer's preference for older or newer matches.

🤖 Recommendation Algorithm

The current recommendation approach is content-based filtering.

Each match is represented as a vector of numerical features.

For example:

Match A:

[intense,
 importance,
 rivalry,
 format,
 players,
 recency,
 ...]

A user's preferences are represented using a vector with the same features.

The system then calculates the cosine similarity between the user preference vector and every match vector.

Conceptually:

User Preference
       ↓
[ 1, 0, 0.22, 0, 0, 1, ... ]
       ↓
Cosine Similarity
       ↓
────────────────────────
Match 1 → 0.766
Match 2 → 0.693
Match 3 → 0.690
Match 4 → 0.687
...
────────────────────────
       ↓
Ranked Recommendations

A higher similarity score means the match is more similar to the user's preferences.

🧪 Example

One test preference profile was created around:

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

The recommendation made sense because the match:

Was a Test
Was classified as intense
Featured Sachin Tendulkar
Featured Rahul Dravid
Featured Virender Sehwag
Was from the older era of Indian cricket

This was one of the first tests of whether the recommendation logic was producing sensible results.

🛠️ Tech Stack
Python
Pandas — data manipulation and preparation
NumPy — numerical operations and vectors
Scikit-learn — cosine similarity
Cricket match data — historical India international matches
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

The raw dataset is kept locally and is not committed to GitHub because of its large file size.

🚀 Getting Started
1. Clone the repository
git clone https://github.com/Aabir265/Cricket-Match-Recommender.git
cd Cricket-Match-Recommender
2. Install dependencies
pip install -r requirements.txt
3. Prepare the dataset
python download_and_prepare.py
4. Run the recommender
python main.py
🔮 Future Improvements

This project is still a work in progress.

Some things I want to improve:

 Build an interactive user preference system
 Allow users to select their favourite players
 Allow users to select a preferred cricket format
 Add an era/classic-cricket preference
 Improve the rivalry/excitement calculation
 Add more match-specific features
 Include batting and bowling performances
 Detect memorable finishes and close chases
 Add links to available match highlights
 Build a simple web interface
 Evaluate recommendation quality with real user feedback
📌 Current Status

Work in Progress 🚧

The core data preparation, feature engineering and first version of the cosine-similarity recommendation system are working.

The next stage is to make the recommendation system more personalized and eventually turn it into an interactive application.

👨‍💻 Author

Aabir Sharma

Built as a project to explore:

Machine Learning
Recommendation Systems
Feature Engineering
Data Analysis
Sports Analytics

⭐ If you find the project interesting, feel free to explore the code or suggest improvements.
