# 🎓 Career Track Student Analytics, BI & Artificial Intelligence Portfolio

[![SQL](https://img.shields.io/badge/SQL-Advanced%20SQL-blue?style=flat&logo=mysql)](https://github.com/)
[![Tableau](https://img.shields.io/badge/Tableau-Dashboard-orange?style=flat&logo=tableau)](https://tableau.com)
[![Python](https://img.shields.io/badge/Python-Pandas%20%7C%20Matplotlib%20%7C%20Seaborn-yellow?style=flat&logo=python)](https://python.org)
[![AI/ML](https://img.shields.io/badge/AI%2FML-Scikit--Learn-success?style=flat&logo=scikit-learn)](https://scikit-learn.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat)]()

---

## 1. 🌐 Project Overview
This comprehensive data analytics and artificial intelligence portfolio project investigates student enrollment trajectories, learning track performance, and retention bottlenecks across three professional career tracks: **Data Scientist**, **Data Analyst**, and **Business Analyst**. The repository provides an end-to-end framework covering relational database design, advanced SQL querying, exploratory data analysis (EDA), predictive modeling using machine learning, and interactive Business Intelligence (BI) dashboards.

---

## 2. 🗄️ Dataset Architecture
The underlying relational database (`sql_and_tableau`) consists of two core normalized tables designed to maintain data integrity and transactional efficiency:
* **`career_track_info`**: A master lookup table mapping professional track IDs to track names (`Data Scientist`, `Data Analyst`, `Business Analyst`).
* **`career_track_student_enrollments`**: A transactional table tracking student registration timestamps (`date_enrolled`) and track completion milestones (`date_completed`).

---

## 3. 🎯 Key Business Questions Addressed
* **Volume & Popularity:** Which professional career track attracts the highest volume of student enrollments?
* **Conversion Success:** What is the overall completion rate percentage for each learning track?
* **Duration & Bottlenecks:** What is the average, minimum, and maximum time-to-completion (measured in days) for students finishing a track?
* **Acquisition Velocity:** Are there seasonal trends or monthly spikes in student registrations over time?
* **Cross-Learning Behavior:** What proportion of students enroll in multiple career tracks simultaneously?
* **Predictive Success Drivers:** Can machine learning accurately forecast whether an incoming student will successfully complete their track based on registration metadata?

---

## 4. 📊 Executive Summary
By synthesizing insights across relational SQL extraction, Python scripting, and Tableau visualization, this project reveals critical behavioral patterns in online professional education:
* **Track Popularity vs. Completion:** While certain tracks command higher upfront enrollment numbers, completion rates vary significantly, highlighting potential engagement drop-offs.
* **Time-to-Completion Efficiency:** Quantifying completion durations enables curriculum directors to identify structural bottlenecks and adjust pacing.
* **Predictive Intelligence:** Implementing a Random Forest classifier allows administrative teams to proactively identify students at risk of drop-off and intervene early.

---

## 📊 Key Findings & Insights
For a detailed, data-backed analysis on student enrollment, track popularity, completion rates, and time-to-completion distributions, check out the [KEY_FINDINGS.md](KEY_FINDINGS.md) file generated from our database pipeline.

---

## 5. 🛠️ Tech Stack & Tools
* **Database & Advanced SQL:** MySQL 8.0 (Schema normalization, Primary/Foreign keys, joins, conditional expressions, date arithmetic via `DATEDIFF`).
* **Data Processing & EDA:** Python (`Pandas`, `NumPy`), Matplotlib, Seaborn.
* **Artificial Intelligence & Machine Learning:** Scikit-Learn (`RandomForestClassifier`, train-test splitting, feature importance scoring, classification metrics).
* **Business Intelligence & KPIs:** Tableau Desktop (Interactive dashboards, conversion funnels, time-to-completion tracking).
* **Version Control:** Git & GitHub.
  
  ---

## 🚀 How to Run the Project Locally

Follow these steps to set up and execute this project on your local machine:

### 1. Database Setup (MySQL)
* Open your MySQL client (e.g., MySQL Workbench).
* Run the script located in `sql/schema.sql` to create the database and tables.
* Execute the analytical queries found in `sql/analysis_queries.sql`.

### 2. Install Python Dependencies & Run Scripts
Install the required libraries and execute the scripts using your terminal:

```bash
pip install -r requirements.txt
python python/exploratory_analysis.py
python python/ai_student_prediction.py

```

---

## 6. 📂 Repository Directory Structure
```text
sql-tableau-career-track-analytics/
│
├── README.md
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── python/
│   ├── exploratory_analysis.py
│   └── ai_student_prediction.py
└── tableau/
    └── dashboard_blueprint.md
