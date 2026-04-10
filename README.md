# 🛡️ DRONA: Eklavya Platform Analytics Dashboard

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**DRONA** is an end-to-end analytics pipeline for the Eklavya EdTech platform. It handles the entire lifecycle of data—from synthetic generation to SQL-based storage and AI-driven behavioral segmentation.

## 📌 Project Overview
DRONA identifies engagement gaps by analyzing how students interact with the platform. Instead of just showing raw numbers, it uses machine learning to categorize students into actionable segments, allowing administrators to prioritize "At-Risk" users before they churn.

---

## ✨ Key Features

* **Real-time KPI Tracking**: Instant visibility into Total Users, Sessions, and Active User Rates using optimized CTE-based SQL queries.
* **Behavioral Trends**: Visualization of Daily Active Users (DAU) and feature-specific adoption (Video Lectures, Quizzes, etc.).
* **School Leaderboard**: Dynamic filtering by school type (Government, Private, Semi-Government) to track regional adoption.
* **🤖 AI Student Segmentation**: Automated $K$-Means clustering that groups students into **Champions**, **Casuals**, and **At-Risk** accounts based on engagement depth and frequency.

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Data Logic** | Python (Pandas, NumPy) |
| **Database** | SQLite3 |
| **Machine Learning** | Scikit-learn ($K$-Means, StandardScaler) |
| **Visualizations** | Plotly Express |

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/git-clone-adi/-DRONA-AD
cd DRONA-Analytics
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
3. Generate the Dataset & Database
   Run the pipeline to simulate the environment:
   ```Bash
   python dataset_gen.py
   ```
   # Generates 150k+ activity rows
```
python db_anal.py
```
  # Migrates CSVs to drona_analytics.db
5. Launch the Dashboard
   ```Bash
   streamlit run app.py
   ```
## 🧠 The Intelligence Layer: K-Means Clustering
The system analyzes 5,000+ users by looking at:
1. **Frequency**: Total number of sessions per student.
2. **Depth**: Total minutes spent on the platform.

The model calculates cluster centroids and automatically maps them to human-readable segments. This ensures that the "At-Risk" label consistently points to students with the lowest activity levels.

---

## 📂 Project Structure
* `app.py`: The main dashboard UI and ML implementation.
* `dataset_gen.py`: Synthetic data engine using weighted random distributions.
* `db_anal.py`: ETL script for database population.
* `check_db.py`: Diagnostic utility for verifying table integrity.
