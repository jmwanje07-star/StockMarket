📊 Stock Market Dashboard

This project showcases a complete data engineering + data visualization pipeline using Python.
Starting from a messy CSV of daily stock prices, the workflow performs cleaning, transformation, aggregation, and interactive visualization using modern tools like Pandas, Parquet, and Streamlit.

⭐ Core Highlights
1. Automated Data Cleaning

Fixes inconsistent and missing values

Standardizes date formats

Normalizes schema

Removes duplicates

Outputs clean, analysis-ready data (cleaned.parquet)

2. Efficient Data Aggregation

Generates optimized Parquet files used by the dashboard:

agg1.parquet → daily average close price per ticker

agg2.parquet → average trading volume by sector

agg3.parquet → daily returns per ticker

3. Interactive Streamlit Dashboard

A rich visualization experience with:

Ticker selection

Date range filtering

Sector filtering

Multiple chart types including:

Area chart

Candlestick chart

Treemap

Horizontal bar chart

Box plot

Scatter plot with color encoding

Multi-ticker trend comparison

Correlation heatmap

4. Lightweight & Reproducible

Fully script-driven

Uses Parquet for fast loading

Clean modular code for easy learning and extension

Ideal for beginners practicing data wrangling, EDA, and dashboard development

🛠️ Project Steps
1. Data Cleaning

Run:

python stock_cleaning.py


Creates:

data/cleaned.parquet

2. Data Aggregation

Run:

python stock_aggregations.py


Creates:

data/agg1.parquet  # Avg daily close by ticker
data/agg2.parquet  # Avg volume by sector
data/agg3.parquet  # Daily returns

3. Visualization (Dashboard)

Run the Streamlit app:

python -m streamlit run app.py


The dashboard will open in your browser with:

Ticker dropdown

Sector filters

Date range selector

Multiple visual analytics

📚 Libraries Used

pandas — data cleaning & transformation

streamlit — interactive dashboard framework

altair — statistical visualizations

plotly — advanced visual charts (scatter, treemap, etc.)

pyarrow — Parquet file handling

🖼️ Example Dashboard Views (Recommended to include screenshots)

Homepage overview

Area chart of average close price

Sector volume treemap

Daily return distribution (box/scatter)

Multi-ticker trend comparison

Correlation heatmap