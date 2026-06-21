# DecodeLabs — Project 3: AI Recommendation Engine
### Tech Stack & Career Recommender | Muskan | Batch 2026

---

## How to Run

```bash
pip install tk          # usually pre-installed with Python
python recommender.py
```

> Requires Python 3.8+ with Tkinter (ships with standard Python on Windows & Linux).

---

## Features Built

| Feature | Description |
|---|---|
| **Preference Rating System** | Rate each selected skill 1–5 stars. Higher-rated skills carry more weight in the TF-IDF vector, making your top skills influence recommendations more strongly. |
| **Similarity Score Display** | Every result card shows a % match score with a colour-coded progress bar (green ≥50%, amber ≥20%, red <20%). |
| **Top 5 Recommendations** | Results are ranked by cosine similarity score, showing only the 5 best matches. |
| **Recommendation Explanation** | Each card shows exactly which of your skills matched the item's tags (highlighted in green), plus additional item tags in grey. |
| **User History** | Every search session is saved to `search_history.json`. The right panel shows your last 15 sessions with a "Re-run" button. |
| **Category Filtering** | Switch between Careers, Courses, Books, and Movies with one click. |
| **Search Bar** | Type any skill and press Enter or click Add. Auto-filters the popular skills chips. |
| **Career Details** | Career cards show salary, region, work mode, job type, experience required, and hiring companies in Pakistan. |

---

## Algorithm

```
Input  →  User skills × star ratings  →  Weighted token list
Process →  TF-IDF vectorization (all corpus + user profile)
         →  Cosine Similarity (dot product / product of norms)
Output  →  Sorted Top-5 list with explanation
```

### Why TF-IDF + Cosine?
- **TF-IDF** rewards specific/rare skills and penalises generic words — more nuanced than raw keyword overlap (Jaccard).
- **Cosine Similarity** is magnitude-invariant, meaning a user with 2 skills vs 10 skills is judged on *direction*, not volume.

---

## Files
```
project3/
├── recommender.py        ← main application (run this)
├── search_history.json   ← auto-created on first run
└── README.md
```
