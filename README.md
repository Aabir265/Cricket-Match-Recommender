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
