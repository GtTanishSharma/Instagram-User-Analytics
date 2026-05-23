# Instagram User Analytics

I analyzed 500 Instagram posts to figure out what actually drives engagement and follower growth. Things like does posting time matter? Do more hashtags mean more reach? Which type of post performs best?

Used Python for the analysis and SQL (SQLite) to query the data.

---

## Files

- `data/instagram_raw_data.csv` — the dataset (500 posts × 13 columns)
- `scripts/analysis.py` — full analysis code
- `outputs/` — all 4 charts generated from the analysis

---

## The Data

500 Instagram post records with these columns:

| Column | What it means |
|---|---|
| Post_Type | Photo, Reel, Carousel, or Story |
| Hashtag_Count | Number of hashtags used |
| Posting_Hour | Hour of day posted (0–23) |
| Day_of_Week | Day posted |
| Followers | Account followers at time of post |
| Caption_Length | Length of caption in characters |
| Likes | Likes received |
| Comments | Comments received |
| Shares | Shares |
| Saves | Saves |
| Reach | Total accounts reached |
| New_Followers | New followers gained from this post |
| Engagement_Rate | (Likes + Comments + Shares) / Reach × 100 |

---

## What I Did

**Data Validation**
- Checked for nulls and duplicates — none found
- Verified all engagement metrics are positive
- Checked data types for each column

**SQL Queries (SQLite)**
- Average engagement broken down by post type
- Top posting hours ranked by engagement rate
- Hashtag count grouped into buckets to find the sweet spot
- Best days of the week to post
- Top 10 highest performing posts

**Python EDA**
- Distribution of engagement rate across all posts
- Scatter plot of likes vs new followers by post type
- Bar chart comparing post types by engagement
- Correlation heatmap across all metrics

---

## What I Found

**Reels dominate everything**

Reels had an average engagement rate of 19.8% compared to 11.8% for Photos. They also brought in more than double the new followers per post. If you're only going to invest in one content type, it's Reels.

**Best time to post is 4pm**

Hour 16 (4pm) had the highest average engagement at 21.4%. Early morning at 4am also performed surprisingly well — probably because there's less competition in the feed at that hour.

**Sunday is the best day**

Sunday had the highest average engagement rate at 18.8%. Monday was the worst at 14.1%.

**Hashtags — more isn't always better**

Interestingly, posts with no hashtags had the highest average engagement (18.2%), followed by posts with 16–30 hashtags. The 1–5 range performed worst. This suggests the algorithm may be deprioritizing hashtag-heavy posts, or that accounts posting without hashtags already have strong organic reach.

**Saves are the strongest signal for follower growth**

In the correlation analysis, Saves had a stronger correlation with New Followers than Likes or Comments. Content that people bookmark is content that converts.

---

## SQL Queries Used

```sql
-- Average engagement by post type
SELECT Post_Type,
       COUNT(*) AS Total_Posts,
       ROUND(AVG(Engagement_Rate), 2) AS Avg_Engagement_Rate,
       ROUND(AVG(New_Followers), 0) AS Avg_New_Followers
FROM instagram_posts
GROUP BY Post_Type
ORDER BY Avg_Engagement_Rate DESC;

-- Best posting hours
SELECT Posting_Hour,
       ROUND(AVG(Engagement_Rate), 2) AS Avg_Engagement
FROM instagram_posts
GROUP BY Posting_Hour
ORDER BY Avg_Engagement DESC
LIMIT 8;

-- Hashtag bucket analysis
SELECT
    CASE
        WHEN Hashtag_Count = 0 THEN 'No Hashtags'
        WHEN Hashtag_Count BETWEEN 1 AND 5 THEN '1-5'
        WHEN Hashtag_Count BETWEEN 6 AND 15 THEN '6-15'
        ELSE '16-30'
    END AS Hashtag_Bucket,
    ROUND(AVG(Engagement_Rate), 2) AS Avg_Engagement
FROM instagram_posts
GROUP BY Hashtag_Bucket
ORDER BY Avg_Engagement DESC;
```

---

## Charts

### Engagement by Post Type
![Post Type](outputs/chart_01_engagement_by_post_type.png)

### Engagement by Posting Hour
![Posting Hour](outputs/chart_02_posting_hour_engagement.png)

### Likes vs New Followers
![Scatter](outputs/chart_03_likes_vs_followers.png)

### Correlation Heatmap
![Heatmap](outputs/chart_04_correlation_heatmap.png)

---

## How to Run

```bash
pip install -r requirements.txt
python scripts/analysis.py
```

Charts will be saved to the `outputs/` folder.

---

## Tools Used

- Python (Pandas, NumPy, Matplotlib, Seaborn)
- SQL via SQLite3 (built into Python — no setup needed)

---

**Tanish Sharma**
B.Sc. Statistics — Delhi University, PGDAV College
[LinkedIn](https://linkedin.com/in/grt-tanish) · Tanishshr1234@gmail.com
