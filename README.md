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
git clone [https://github.com/YOUR_USERNAME/DRONA-Analytics.git](https://github.com/YOUR_USERNAME/DRONA-Analytics.git)
cd DRONA-Analytics
