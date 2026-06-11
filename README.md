# Bluestock Mutual Fund Analytics Capstone

## Overview

An end-to-end Mutual Fund Analytics platform built using Python, SQLite, Pandas, SQL, Jupyter Notebook, and Power BI.

The project analyzes mutual fund performance, investor behavior, risk metrics, and portfolio concentration while providing interactive dashboards and recommendation capabilities.

---

## Features

- Data Cleaning Pipeline
- SQLite Data Warehouse
- Exploratory Data Analysis
- Performance Analytics
- VaR and CVaR Analysis
- Rolling Sharpe Ratio
- Investor Cohort Analysis
- SIP Continuity Analysis
- Fund Recommendation Engine
- Power BI Dashboard

---

## Project Structure

data/
- raw/
- processed/
- db/

notebooks/
- 03_eda_analysis.ipynb
- Performance_Analytics.ipynb
- Advanced_Analytics.ipynb

scripts/
- live_nav_fetch.py
- data_cleaning.py
- load_sqlite.py
- run_queries.py
- recommender.py

sql/
- schema.sql
- queries.sql

reports/
- fund_scorecard.csv
- alpha_beta.csv
- var_cvar_report.csv
- rolling_sharpe_chart.png

---

## Installation

pip install -r requirements.txt

---

## Run ETL Pipeline

python scripts/data_cleaning.py

python scripts/load_sqlite.py

python scripts/run_queries.py

---

## Run Recommender

python scripts/recommender.py

Input:
Low / Moderate / High

Output:
Top 3 recommended funds based on Sharpe Ratio.

---

## Technologies

- Python
- Pandas
- NumPy
- SQLite
- SQLAlchemy
- Plotly
- Matplotlib
- Seaborn
- Jupyter
- Power BI

---

## Author

Sankalp Raj Singh
Bluestock Mutual Fund Analytics Capstone