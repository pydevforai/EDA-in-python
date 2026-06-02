# 🏏 PSL 2022 Data Analysis & Visualization

A data analysis project exploring **Pakistan Super League (PSL) 2022** match-level data using Python, Pandas, and Seaborn to derive meaningful insights about team performances, player stats, and venue trends.

---

## 📌 About PSL

The **Pakistan Super League (PSL)** is a professional T20 cricket league sanctioned by the **Pakistan Cricket Board (PCB)**. Founded in **2015**, the league features six franchises representing major cities of Pakistan:

| Team | City | Home Ground |
|---|---|---|
| Karachi Kings | Karachi | National Stadium |
| Lahore Qalandars | Lahore | Gaddafi Stadium |
| Quetta Gladiators | Quetta | National Stadium |
| Peshawar Zalmi | Peshawar | Arbab Niaz Stadium |
| Islamabad United | Islamabad | Rawalpindi Cricket Stadium |
| Multan Sultans | Multan | Multan Cricket Stadium |

---

## 📂 Project Structure

```
PSL-Data-Analysis/
├── Data_Visualisation_project.ipynb   # Main analysis notebook
├── PSL.csv                            # Dataset (34 matches)
└── README.md                          # Project documentation
```

---

## 📊 Dataset Overview

The dataset contains **34 matches** from PSL 2022 including Group Stage, Playoffs, and the Final.

| Column | Type | Description |
|---|---|---|
| match_id | int | Unique match number |
| date | string | Match date |
| venue | string | Stadium name |
| stage | string | Group / Playoff / Final |
| team1 | string | First team |
| team2 | string | Second team |
| toss_winner | string | Team that won the toss |
| toss_decision | string | Bat or Field |
| first_ings_score | int | First innings total runs |
| first_ings_wkts | int | First innings wickets lost |
| second_ings_score | int | Second innings total runs |
| second_ings_wkts | int | Second innings wickets lost |
| match_winner | string | Winning team |
| won_by | string | Runs or Wickets |
| margin | int | Winning margin |
| player_of_the_match | string | Best player of the match |
| top_scorer | string | Highest run scorer |
| highscore | int | Highest individual score |
| best_bowling | string | Best bowler of the match |
| best_bowling_figure | string | Bowling figures (wickets--runs) |

---

## 🔍 Analysis Performed

### 🧹 Data Wrangling
- Created a `teams_info` table with City and Home Ground
- Merged with main dataframe using **Left Join** on `match_winner`
- Extracted wickets from bowling figures using `lambda` function

### 📈 Visualizations & Questions Answered

| # | Question | Chart Type |
|---|---|---|
| 1 | Which city's team won the most matches? | Bar Chart |
| 2 | Which PSL team won the most matches? | Horizontal Bar Chart |
| 3 | Toss Decision Trends | Count Plot |
| 4 | Does winning the toss help win the match? | Percentage + Table |
| 5 | How do teams win — Runs or Wickets? | Count Plot |
| 6 | Top 10 Player of the Match awards | Horizontal Bar Chart |
| 7 | Top 2 highest scorers | Horizontal Bar Chart |
| 8 | Top 5 best bowlers by wickets | Horizontal Bar Chart |
| 9 | Which venue hosted the most matches? | Bar Chart |

### ❓ Custom Questions
- **Q1** — Which team won by the highest margin of runs?
- **Q2** — Which player had the highest individual score?
- **Q3** — Which bowler had the best bowling figures?
- **Q4** — Which venue hosted the most matches?
- **Q5** — How many matches were won by Runs vs Wickets?
- **Q6** — Which teams played the Final and who won?
- **Q7** — What was the average first innings score? *(with distribution chart)*

---

## 🛠️ Libraries Used

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

---

## ▶️ How to Run

1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
```

2. Go into the project folder
```bash
cd PSL-Data-Analysis
```

3. Install required libraries
```bash
pip install pandas numpy matplotlib seaborn
```

4. Open the notebook
```bash
jupyter notebook Data_Visualisation_project.ipynb
```

---

## 💡 Key Insights

- Toss winner wins the match only **~41%** of the time — toss is not a big advantage
- Most matches were won by **Runs** rather than Wickets
- **Gaddafi Stadium, Lahore** hosted the most matches including the Final
- Average first innings score across all matches was around **166 runs**

---

## 👤 Author

**Your Name**
- 📧 your.email@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/your-profile)
- 🐙 [GitHub](https://github.com/your-username)

---

> ⭐ If you found this project useful, please give it a star on GitHub!
