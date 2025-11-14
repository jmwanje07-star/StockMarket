import pandas as pd
import re

# ---------------------------------------------------------
# 1. Load raw CSV from GitHub
# ---------------------------------------------------------
url = "https://raw.githubusercontent.com/gchandra10/filestorage/refs/heads/main/stock_market.csv"
df = pd.read_csv(url)

print("Shape:", df.shape)
print(df.head())
print(df.info())

# ---------------------------------------------------------
# 2. Normalize column names: trim, lowercase, replace spaces with underscores
# ---------------------------------------------------------
df.columns = [re.sub(r'\s+', '_', c.strip().lower()) for c in df.columns]

# ---------------------------------------------------------
# 3. Standardize common missing-value placeholders → pd.NA
# ---------------------------------------------------------
df = df.replace(["", " ", "na", "n/a", "none", "null", "-", "<na>"], pd.NA)

# ---------------------------------------------------------
# 4. Clean string columns: trim whitespace + lowercase
# ---------------------------------------------------------
for col in df.select_dtypes(include="object"):
    df[col] = df[col].astype(str).str.strip().str.lower()

# Re-clean after transformations (catch new "nan", "null", etc.)
df = df.replace(["na", "nan", "none", "-", "<na>", "null"], pd.NA)

# ---------------------------------------------------------
# 5. Convert trade_date → datetime (format: YYYY-MM-DD)
# ---------------------------------------------------------
df['trade_date'] = pd.to_datetime(df['trade_date'], errors='coerce').dt.strftime("%Y-%m-%d")

# ---------------------------------------------------------
# 6. Remove duplicate rows and rows missing essential fields
# ---------------------------------------------------------
df = df.drop_duplicates().dropna(subset=['trade_date', 'ticker'])

# ---------------------------------------------------------
# 7. Convert numeric columns to proper numeric dtype
# ---------------------------------------------------------
numeric_cols = ['open_price', 'close_price', 'volume']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Option: Drop rows where all three numeric fields are missing
df = df.dropna(subset=['open_price', 'close_price', 'volume'], how='all')

# ---------------------------------------------------------
# 8. Save final cleaned Parquet file
# ---------------------------------------------------------
df.to_parquet("data/cleaned.parquet", index=False)

print("Cleaned data saved to data/cleaned.parquet")
print(f"Final shape: {df.shape}")
print(f"Unique tickers: {df['ticker'].nunique()}")
