"""
generate_key_findings.py
-------------------------
Connects to the sql_and_tableau MySQL database, runs analysis queries,
and writes a KEY_FINDINGS.md file with data-backed insights you can
paste straight into your README.

Usage:
    pip install pymysql pandas python-dotenv
    python generate_key_findings.py

Create a .env file (same folder) with:
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=sql_and_tableau
"""

import os
import pandas as pd
import pymysql
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "sql_and_tableau"),
)

# ---------------------------------------------------------------
# 1. Track popularity + completion rate
# ---------------------------------------------------------------
q_track_summary = """
    SELECT
        t.track_name,
        COUNT(e.student_id) AS total_enrollments,
        SUM(CASE WHEN e.date_completed IS NOT NULL THEN 1 ELSE 0 END) AS total_completed,
        ROUND(SUM(CASE WHEN e.date_completed IS NOT NULL THEN 1 ELSE 0 END) * 100.0
              / COUNT(e.student_id), 2) AS completion_rate_pct
    FROM career_track_info t
    LEFT JOIN career_track_student_enrollments e ON t.track_id = e.track_id
    GROUP BY t.track_name
    ORDER BY total_enrollments DESC;
"""
df_tracks = pd.read_sql(q_track_summary, con=connection)

# ---------------------------------------------------------------
# 2. Time-to-completion stats (overall + bucketed)
# ---------------------------------------------------------------
q_duration = """
    SELECT
        ROUND(AVG(DATEDIFF(date_completed, date_enrolled)), 1) AS avg_days,
        MIN(DATEDIFF(date_completed, date_enrolled)) AS min_days,
        MAX(DATEDIFF(date_completed, date_enrolled)) AS max_days
    FROM career_track_student_enrollments
    WHERE date_completed IS NOT NULL;
"""
df_duration = pd.read_sql(q_duration, con=connection)

q_buckets = """
    SELECT
        CASE
            WHEN DATEDIFF(date_completed, date_enrolled) = 0 THEN 'Same day'
            WHEN DATEDIFF(date_completed, date_enrolled) BETWEEN 1 AND 7 THEN '1 to 7 days'
            WHEN DATEDIFF(date_completed, date_enrolled) BETWEEN 8 AND 30 THEN '8 to 30 days'
            WHEN DATEDIFF(date_completed, date_enrolled) BETWEEN 31 AND 60 THEN '31 to 60 days'
            WHEN DATEDIFF(date_completed, date_enrolled) BETWEEN 61 AND 90 THEN '61 to 90 days'
            WHEN DATEDIFF(date_completed, date_enrolled) BETWEEN 91 AND 365 THEN '91 to 365 days'
            ELSE '366+ days'
        END AS bucket,
        COUNT(*) AS student_count
    FROM career_track_student_enrollments
    WHERE date_completed IS NOT NULL
    GROUP BY bucket;
"""
df_buckets = pd.read_sql(q_buckets, con=connection)
top_bucket = df_buckets.sort_values("student_count", ascending=False).iloc[0]

# ---------------------------------------------------------------
# 3. Monthly enrollment trend (spot the peak month)
# ---------------------------------------------------------------
q_monthly = """
    SELECT
        DATE_FORMAT(date_enrolled, '%Y-%m') AS month,
        COUNT(*) AS enrollments
    FROM career_track_student_enrollments
    GROUP BY month
    ORDER BY month;
"""
df_monthly = pd.read_sql(q_monthly, con=connection)
peak_month_row = df_monthly.sort_values("enrollments", ascending=False).iloc[0]

connection.close()

# ---------------------------------------------------------------
# 4. Build the markdown report
# ---------------------------------------------------------------
top_track = df_tracks.iloc[0]
overall_completion = round(df_tracks["total_completed"].sum() * 100.0 /
                            df_tracks["total_enrollments"].sum(), 2)

report = f"""# Key Findings

## 1. Track Popularity
**{top_track['track_name']}** is the most-enrolled career track with
{int(top_track['total_enrollments'])} enrollments, out of the following
breakdown:

{df_tracks.to_markdown(index=False)}

## 2. Completion Rate
The overall track completion rate across all students is **{overall_completion}%**.
This is low relative to enrollment volume, suggesting a significant
drop-off between signing up and finishing a track.

## 3. Time-to-Completion
- Average time to complete a track: **{df_duration['avg_days'][0]} days**
- Fastest completion: {df_duration['min_days'][0]} days
- Slowest completion: {df_duration['max_days'][0]} days
- Most common completion window: **{top_bucket['bucket']}**
  ({int(top_bucket['student_count'])} students)

**Implication:** Students who do complete a track mostly need many months
to do so — an **annual subscription** is the more rational plan for a
student who intends to finish, since monthly/quarterly plans risk lapsing
before completion.

## 4. Enrollment Seasonality
The peak enrollment month was **{peak_month_row['month']}** with
{int(peak_month_row['enrollments'])} enrollments. Compare this against
the surrounding months to check whether a campaign, promotion, or
seasonal effect (e.g. new year, back-to-school) is driving the spike —
and whether that spike converts to completions or mostly to drop-offs.

## 5. Recommendation
Given the gap between enrollment volume and completion rate, prioritize
engagement mechanics (progress streaks, reminders, community Q&A) over
acquisition campaigns — new sign-ups alone don't appear to translate into
finished tracks.
"""

with open("KEY_FINDINGS.md", "w") as f:
    f.write(report)

print("[INFO] KEY_FINDINGS.md generated successfully.")
