import pandas as pd

# ---------------------------------------------------------
# 1. Load cleaned parquet file
# ---------------------------------------------------------
df = pd.read_parquet("data/cleaned.parquet")

# Ensure consistent lowercase column names
df.columns = [c.lower() for c in df.columns]

# ---------------------------------------------------------
# 2. Aggregation 1: Average close price per (date, ticker)
# ---------------------------------------------------------
# Group by trade_date and ticker → compute mean close_price
agg1 = df.groupby(['trade_date', 'ticker'], as_index=False)['close_price'].mean()

# Save result
agg1.to_parquet("data/agg1.parquet", index=False)

# ---------------------------------------------------------
# 3. Aggregation 2: Average traded volume per sector
# ---------------------------------------------------------
agg2 = df.groupby('sector', as_index=False)['volume'].mean()

# Save result
agg2.to_parquet("data/agg2.parquet", index=False)

# ---------------------------------------------------------
# 4. Aggregation 3: Daily return per ticker
# ---------------------------------------------------------
# Sort by ticker + date to compute returns in correct order
df_sorted = df.sort_values(['ticker', 'trade_date'])

# Compute percent change of close_price within each ticker
df_sorted['daily_return'] = df_sorted.groupby('ticker')['close_price'].pct_change()

# Keep only required columns and drop NaNs (first day has no return)
agg3 = df_sorted[['trade_date', 'ticker', 'daily_return']].dropna()

# Save result
agg3.to_parquet("data/agg3.parquet", index=False)

# ---------------------------------------------------------
# 5. Status message
# ---------------------------------------------------------
print("Aggregations saved to data/agg1.parquet, data/agg2.parquet, data/agg3.parquet")
