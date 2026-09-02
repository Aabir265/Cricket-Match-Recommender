🏏 Cricket Match Recommender

A content-based recommendation system that recommends **must-watch India cricket matches** based on what a viewer is interested in.

The idea behind this project is simple:

&gt; There are hundreds of India matches from the past. If someone wants to watch highlights but doesn't know which match to pick, why not recommend one based on what they like?

For example, a viewer might prefer:

- Intense matches
- Test cricket
- Classic Indian cricket
- Matches involving Sachin Tendulkar or Rahul Dravid
- Certain opponents
- Older or more recent matches

The system converts these preferences into numerical feature vectors and uses **cosine similarity** to find matches that are most similar to the viewer's preferences.

---

## 📊 Dataset

The current dataset contains:

- **1,020 India international matches**
- **526 ODIs**
- **276 T20Is**
- **218 Tests**
- Matches spanning **2001–2026**
- 15 different opponents

The dataset currently covers matches from:

```text
2001-12-19 → 2026-08-15
The raw dataset is prepared before being used by the recommendation system.
The large raw dataset is intentionally not stored in this repository because of its file size.

🧠 Feature Engineering
Each match is represented using numerical features.
🔥 Match Intensity
A match is considered intense when the winning margin is relatively small.
Current rules:
Win by wickets → margin &lt; 5 wickets
Win by runs    → margin &lt; 25 runs
This produces a binary feature:
1 → Intense
0 → Not intense
The current dataset contains:
204 intense matches
816 non-intense matches

🏆 Match Importance
A match receives an importance score based on whether it was:


A Final


A Semi Final


Played at selected historically significant venues


The feature is represented as:
1 → Important
0 → Not important
The current dataset contains:
124 important matches
896 non-important matches



          
            
          
        
  
        
    

⚔️ Opponent Excitement / Rivalry
Instead of manually assigning a rivalry score to every opponent, the current system derives it from the dataset.
The score is based on the percentage of India's matches against an opponent that were classified as intense.
For example:
Opponent → Intense Match Rate

West Indies → 23.93%
Ireland     → 23.08%
Zimbabwe    → 22.50%
Australia   → 22.22%
England     → 21.19%
South Africa → 20.34%
Pakistan    → 18.84%
New Zealand → 18.02%
Sri Lanka   → 16.67%
Bangladesh  → 16.39%
Opponents with very few matches are excluded from the calculation to avoid unreliable percentages caused by small sample sizes.

🏏 Match Format
The format is converted into numerical features:
odi_format
t20_format
test_format
For example:
Test → 0 0 1
ODI  → 1 0 0
T20I → 0 1 0
This avoids treating formats as ordered numerical values.

👤 Player Features
The system also considers whether selected players were part of India's playing XI.
Current player features include:


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




          
            
          
        
  
        
    

🕐 Recency
The match year is normalized between 0 and 1.
Older matches receive values closer to 0, while newer matches receive values closer to 1.
This allows the recommendation system to consider a viewer's preference for older or newer matches without treating newer matches as automatically better.

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
The current system compares the user preference vector against all 1,020 matches and ranks them according to their similarity scores.

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
The match was recommended with a cosine similarity score of approximately:
0.766
The recommendation made sense because the match:


Was a Test


Was classified as intense


Featured Sachin Tendulkar


Featured Rahul Dravid


Featured Virender Sehwag


Was from the older era of Indian cricket


This was one of the first tests of whether the recommendation logic was producing sensible results.

📈 Current Feature Matrix
The current system uses 15 numerical features for every match.
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
The resulting feature matrix has the shape:
(1020, 15)
Meaning:
1,020 matches × 15 features
Missing rivalry values are currently handled by filling them with 0 before calculating cosine similarity.

🔢 User Preference Vector
A user preference is represented using the same 15 features as the match vectors.
For example:
{
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
The preference vector is then compared against every match vector using cosine similarity.

🛠️ Tech Stack


Python — core programming language


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
Planned improvements include:


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


 Improve personalization


 Experiment with feature weighting


 Evaluate recommendation quality with real user feedback



📌 Current Status
Work in Progress 🚧
The core data preparation, feature engineering and first version of the cosine-similarity recommendation system are working.
Currently, the system can:
✓ Prepare historical India match data
✓ Engineer numerical match features
✓ Create a feature matrix
✓ Create a user preference vector
✓ Calculate cosine similarity
✓ Rank matches based on similarity
The next stage is to make the recommendation system more personalized and eventually turn it into an interactive application.

🎯 Project Motivation
This project started from a simple question:

"I want to watch an India cricket match from the past. Which one should I watch?"

There are hundreds of matches to choose from, and different viewers may have completely different preferences.
Someone might want:

"Give me an intense India vs Australia Test."

Another person might want:

"Show me a classic Sachin Tendulkar match."

Someone else might prefer:

"Give me a recent high-pressure T20I."

The goal is to eventually make the recommendation system flexible enough to understand these different preferences.

👨‍💻 Author
Aabir Sharma
Built as a project to explore:


Machine Learning


Recommendation Systems


Feature Engineering


Data Analysis


Sports Analytics



⭐ If you find the project interesting, feel free to explore the code or suggest improvements.
Built with Python, cricket, and a lot of curiosity. 🏏
