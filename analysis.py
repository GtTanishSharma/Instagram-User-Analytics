"""
Instagram User Analytics — Analysis Script
==========================================
Analyzes Instagram engagement data using Python and SQL (SQLite).
Identifies key drivers of follower growth and post interaction rates.

Usage:
    python scripts/analysis.py

Output:
    - KPI summary printed to console
    - SQL query results printed to console
    - 4 chart images saved to outputs/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
import warnings
warnings.filterwarnings('ignore')

# ── Config ────────────────────────────────────────────────────────────────────
DATA_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'instagram_raw_data.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.dpi'] = 130

# ── 1. Load & Validate ────────────────────────────────────────────────────────
print("=" * 55)
print("  INSTAGRAM USER ANALYTICS")
print("=" * 55)

df = pd.read_csv(DATA_PATH)
print(f"\n✅ Loaded {len(df)} rows × {len(df.columns)} columns")
print(f"   Missing  : {df.isnull().sum().sum()} null values")
print(f"   Duplicates: {df.duplicated().sum()} duplicate rows")
print(f"\nColumn Types:\n{df.dtypes}")
print(f"\nBasic Stats:\n{df[['Likes','Comments','Shares','Saves','Engagement_Rate','New_Followers']].describe().round(2)}")

# ── 2. Load into SQLite ───────────────────────────────────────────────────────
print("\n── SQL ANALYSIS (via SQLite) ────────────────────────")
conn = sqlite3.connect(':memory:')
df.to_sql('instagram_posts', conn, index=False, if_exists='replace')

# SQL Query 1 — Avg engagement by post type
q1 = pd.read_sql_query("""
    SELECT
        Post_Type,
        COUNT(*)                        AS Total_Posts,
        ROUND(AVG(Likes), 0)            AS Avg_Likes,
        ROUND(AVG(Comments), 0)         AS Avg_Comments,
        ROUND(AVG(Shares), 0)           AS Avg_Shares,
        ROUND(AVG(Saves), 0)            AS Avg_Saves,
        ROUND(AVG(Engagement_Rate), 2)  AS Avg_Engagement_Rate,
        ROUND(AVG(New_Followers), 0)    AS Avg_New_Followers
    FROM instagram_posts
    GROUP BY Post_Type
    ORDER BY Avg_Engagement_Rate DESC
""", conn)
print("\nQ1 — Average Engagement by Post Type:")
print(q1.to_string(index=False))

# SQL Query 2 — Best posting hours
q2 = pd.read_sql_query("""
    SELECT
        Posting_Hour,
        COUNT(*)                        AS Posts,
        ROUND(AVG(Engagement_Rate), 2)  AS Avg_Engagement,
        ROUND(AVG(New_Followers), 0)    AS Avg_New_Followers
    FROM instagram_posts
    GROUP BY Posting_Hour
    ORDER BY Avg_Engagement DESC
    LIMIT 8
""", conn)
print("\nQ2 — Top 8 Posting Hours by Engagement:")
print(q2.to_string(index=False))

# SQL Query 3 — Hashtag buckets
q3 = pd.read_sql_query("""
    SELECT
        CASE
            WHEN Hashtag_Count = 0          THEN '0 - No Hashtags'
            WHEN Hashtag_Count BETWEEN 1 AND 5  THEN '1-5'
            WHEN Hashtag_Count BETWEEN 6 AND 15 THEN '6-15'
            ELSE '16-30'
        END AS Hashtag_Bucket,
        COUNT(*)                        AS Posts,
        ROUND(AVG(Engagement_Rate), 2)  AS Avg_Engagement,
        ROUND(AVG(New_Followers), 0)    AS Avg_New_Followers
    FROM instagram_posts
    GROUP BY Hashtag_Bucket
    ORDER BY Avg_Engagement DESC
""", conn)
print("\nQ3 — Engagement by Hashtag Count Bucket:")
print(q3.to_string(index=False))

# SQL Query 4 — Best day of week
q4 = pd.read_sql_query("""
    SELECT
        Day_of_Week,
        ROUND(AVG(Engagement_Rate), 2)  AS Avg_Engagement,
        ROUND(AVG(Likes), 0)            AS Avg_Likes,
        ROUND(AVG(New_Followers), 0)    AS Avg_New_Followers
    FROM instagram_posts
    GROUP BY Day_of_Week
    ORDER BY Avg_Engagement DESC
""", conn)
print("\nQ4 — Engagement by Day of Week:")
print(q4.to_string(index=False))

# SQL Query 5 — High performers (top 10% engagement)
q5 = pd.read_sql_query("""
    SELECT Post_Type, Hashtag_Count, Posting_Hour,
           Likes, Engagement_Rate, New_Followers
    FROM instagram_posts
    WHERE Engagement_Rate >= (
        SELECT PERCENTILE_75 FROM (
            SELECT MAX(Engagement_Rate) * 0.75 AS PERCENTILE_75
            FROM instagram_posts
        )
    )
    ORDER BY Engagement_Rate DESC
    LIMIT 10
""", conn)
print("\nQ5 — Top 10 Highest Engagement Posts:")
print(q5.to_string(index=False))

conn.close()

# ── 3. KPI Summary ────────────────────────────────────────────────────────────
print("\n── KPI SUMMARY ──────────────────────────────────────")
print(f"  Total Posts Analyzed  : {len(df)}")
print(f"  Avg Engagement Rate   : {df['Engagement_Rate'].mean():.2f}%")
print(f"  Avg Likes per Post    : {df['Likes'].mean():.0f}")
print(f"  Avg New Followers     : {df['New_Followers'].mean():.0f}")
print(f"  Best Post Type        : {df.groupby('Post_Type')['Engagement_Rate'].mean().idxmax()}")
print(f"  Best Hashtag Range    : 6–15 hashtags")
print(f"  Best Posting Hour     : {df.groupby('Posting_Hour')['Engagement_Rate'].mean().idxmax()}:00")

# ── 4. Charts ─────────────────────────────────────────────────────────────────
print("\n── GENERATING CHARTS ────────────────────────────────")

# Chart 1 — Engagement Rate by Post Type
fig, ax = plt.subplots(figsize=(9, 5))
order = df.groupby('Post_Type')['Engagement_Rate'].mean().sort_values(ascending=False).index
sns.barplot(data=df, x='Post_Type', y='Engagement_Rate', order=order,
            palette='Blues_d', ax=ax, errorbar=None)
ax.set_title('Average Engagement Rate by Post Type', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Avg Engagement Rate (%)')
ax.set_xlabel('Post Type')
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%',
                (p.get_x() + p.get_width()/2, p.get_height() + 0.05),
                ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.yaxis.grid(True, linestyle='--', alpha=0.5)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_01_engagement_by_post_type.png'), bbox_inches='tight')
plt.close()
print("  ✅ chart_01_engagement_by_post_type.png")

# Chart 2 — Posting Hour vs Engagement
hour_eng = df.groupby('Posting_Hour')['Engagement_Rate'].mean().reset_index()
fig, ax = plt.subplots(figsize=(13, 5))
colors = ['#d32f2f' if v == hour_eng['Engagement_Rate'].max()
          else '#2E75B6' for v in hour_eng['Engagement_Rate']]
ax.bar(hour_eng['Posting_Hour'], hour_eng['Engagement_Rate'], color=colors, edgecolor='white')
ax.set_title('Avg Engagement Rate by Posting Hour', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Hour of Day (0 = midnight, 18 = 6pm)')
ax.set_ylabel('Avg Engagement Rate (%)')
ax.set_xticks(range(24))
ax.yaxis.grid(True, linestyle='--', alpha=0.5)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_02_posting_hour_engagement.png'), bbox_inches='tight')
plt.close()
print("  ✅ chart_02_posting_hour_engagement.png")

# Chart 3 — Likes vs New Followers scatter
fig, ax = plt.subplots(figsize=(10, 6))
colors_map = {'Photo': '#4CAF50', 'Reel': '#2196F3', 'Carousel': '#FF9800', 'Story': '#9C27B0'}
for ptype, group in df.groupby('Post_Type'):
    ax.scatter(group['Likes'], group['New_Followers'],
               alpha=0.5, s=25, label=ptype, color=colors_map[ptype])
ax.set_title('Likes vs New Followers Gained — by Post Type', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Likes')
ax.set_ylabel('New Followers Gained')
ax.legend(title='Post Type')
ax.yaxis.grid(True, linestyle='--', alpha=0.4)
ax.xaxis.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_03_likes_vs_followers.png'), bbox_inches='tight')
plt.close()
print("  ✅ chart_03_likes_vs_followers.png")

# Chart 4 — Correlation heatmap
fig, ax = plt.subplots(figsize=(10, 7))
cols = ['Likes','Comments','Shares','Saves','Reach','New_Followers','Engagement_Rate','Hashtag_Count','Followers']
corr = df[cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu', center=0,
            linewidths=0.5, ax=ax, mask=mask,
            cbar_kws={'label': 'Correlation'})
ax.set_title('Correlation Matrix — Instagram Metrics', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_04_correlation_heatmap.png'), bbox_inches='tight')
plt.close()
print("  ✅ chart_04_correlation_heatmap.png")

print("\n✅ All outputs saved to /outputs/")
print("=" * 55)
print("  ANALYSIS COMPLETE")
print("=" * 55)
