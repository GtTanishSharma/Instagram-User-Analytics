# Instagram User Analytics

Wanted to understand what actually makes Instagram posts perform well. So I took 500 posts worth of data and dug into it using Python and SQL.

The questions I was trying to answer were pretty straightforward — does post type matter? What time should you post? Do hashtags actually help? What leads to gaining new followers?

---

## What I used

Python, Pandas, SQLite for the SQL queries, Matplotlib and Seaborn for charts.

---

## The dataset

500 posts with 13 columns — post type, hashtags used, hour posted, day of week, followers, likes, comments, shares, saves, reach, new followers gained, and engagement rate.

Engagement rate here means likes plus comments plus shares divided by reach. I used reach instead of followers because reach tells you how many people actually saw the post, not just how many could have.

---

## What I did

Loaded the data, checked for nulls and duplicates, verified the engagement rate formula matched the column values.

Then loaded everything into a SQLite database and queried it — average engagement by post type, best hours to post, hashtag count analysis, best days of the week. After that did some EDA in Pandas and built four charts.

---

## What I found

**Reels are not even close**

19.8% average engagement rate vs 11.8% for Photos. Reels also brought in more than double the new followers per post. If I had to pick one format it would be Reels every time.

**4pm is the best time**

Hour 16 had the highest average engagement across all posts. 4am surprisingly also performed well — probably because there are fewer posts competing for attention at that hour.

**Sunday over Monday**

Sunday averaged 18.8% engagement. Monday was the worst at 14.1%. People are more active on weekends, which makes sense.

**Saves matter more than I expected**

When I looked at what correlates most with gaining new followers, saves came in almost as strong as likes. People who bookmark your content are more likely to follow you. So content worth saving is probably more valuable than content worth liking.

**Hashtags were interesting**

Posts with no hashtags had the highest average engagement at 18.2%. The 1 to 5 hashtag range performed worst. I expected the opposite. Either the algorithm has moved on from hashtag discovery, or the accounts posting without hashtags are already strong enough to not need them.

---

## Files

- `data/instagram_raw_data.csv` — the dataset
- `scripts/analysis.py` — all the code
- `outputs/` — the four charts

---

## How to run

```
pip install -r requirements.txt
python scripts/analysis.py
```

---

**Tanish Sharma**
[LinkedIn](https://linkedin.com/in/grt-tanish) · Tanishshr1234@gmail.com
