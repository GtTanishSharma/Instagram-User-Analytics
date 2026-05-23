import numpy as np
import pandas as pd
import os

np.random.seed(7)
n = 500

post_types   = np.random.choice(['Photo', 'Reel', 'Carousel', 'Story'], n, p=[0.3, 0.4, 0.2, 0.1])
hashtag_count = np.random.randint(0, 30, n)
posting_hour  = np.random.choice(range(24), n)
day_of_week   = np.random.choice(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], n)
followers     = np.random.randint(500, 100000, n)
caption_len   = np.random.randint(0, 500, n)

base_likes  = followers * np.random.uniform(0.01, 0.15, n)
type_boost  = np.where(post_types=='Reel', 1.8,
              np.where(post_types=='Carousel', 1.3, 1.0))
likes       = (base_likes * type_boost).astype(int)
comments    = (likes * np.random.uniform(0.02, 0.10, n)).astype(int)
shares      = (likes * np.random.uniform(0.01, 0.05, n)).astype(int)
saves       = (likes * np.random.uniform(0.05, 0.20, n)).astype(int)
reach       = (followers * np.random.uniform(0.3, 1.5, n)).astype(int)
new_followers = (likes * np.random.uniform(0.002, 0.02, n)).astype(int)
engagement_rate = ((likes + comments + shares) / reach * 100).round(2)

df = pd.DataFrame({
    'Post_Type': post_types,
    'Hashtag_Count': hashtag_count,
    'Posting_Hour': posting_hour,
    'Day_of_Week': day_of_week,
    'Followers': followers,
    'Caption_Length': caption_len,
    'Likes': likes,
    'Comments': comments,
    'Shares': shares,
    'Saves': saves,
    'Reach': reach,
    'New_Followers': new_followers,
    'Engagement_Rate': engagement_rate
})

out = os.path.join(os.path.dirname(__file__), 'instagram_raw_data.csv')
df.to_csv(out, index=False)
print(f"Generated {len(df)} rows → {out}")
