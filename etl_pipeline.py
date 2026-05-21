import pandas as pd
import numpy as np
from scipy import stats

# ─────────────────────────────────────
# 1. LOAD
# ─────────────────────────────────────
def load_data(path="data/financial_records.csv"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    print(f"Loaded {len(df)} records")
    return df

# ─────────────────────────────────────
# 2. CLEAN
# ─────────────────────────────────────
def clean_data(df):
    before = len(df)
    df.drop_duplicates(subset="record_id", inplace=True)
    df.dropna(subset=["amount", "date", "category"], inplace=True)
    df = df[df["amount"] > 0]
    print(f"Cleaned: {before - len(df)} rows removed. Remaining: {len(df)}")
    return df

# ─────────────────────────────────────
# 3. OUTLIER DETECTION (Z-Score + IQR)
# ─────────────────────────────────────
def detect_outliers(df):
    # Z-Score method
    df["z_score"] = np.abs(stats.zscore(df["amount"]))
    df["is_outlier_zscore"] = df["z_score"] > 3

    # IQR method
    Q1 = df["amount"].quantile(0.25)
    Q3 = df["amount"].quantile(0.75)
    IQR = Q3 - Q1
    df["is_outlier_iqr"] = (df["amount"] < Q1 - 1.5 * IQR) | (df["amount"] > Q3 + 1.5 * IQR)

    n_outliers = df["is_outlier_zscore"].sum()
    print(f"Outliers detected (Z-Score): {n_outliers}")
    print(f"Outliers detected (IQR)    : {df['is_outlier_iqr'].sum()}")
    return df

# ─────────────────────────────────────
# 4. NORMALIZATION
# ─────────────────────────────────────
def normalize(df):
    # Min-Max normalization
    df["amount_minmax"] = (df["amount"] - df["amount"].min()) / \
                          (df["amount"].max() - df["amount"].min())

    # Z-Score normalization
    df["amount_zscore_norm"] = (df["amount"] - df["amount"].mean()) / df["amount"].std()

    # Log transform (handles skewness)
    df["amount_log"] = np.log1p(df["amount"])
    return df

# ─────────────────────────────────────
# 5. FEATURE ENGINEERING
# ─────────────────────────────────────
def feature_engineering(df):
    df["year"]          = df["date"].dt.year
    df["month"]         = df["date"].dt.month
    df["quarter"]       = df["date"].dt.quarter
    df["day_of_week"]   = df["date"].dt.dayofweek
    df["month_str"]     = df["date"].dt.to_period("M").astype(str)

    # Budget variance
    df["budget_variance"]     = df["amount"] - df["budget"]
    df["budget_variance_pct"] = (df["budget_variance"] / df["budget"]) * 100
    df["over_budget"]         = (df["budget_variance"] > 0).astype(int)

    # Rolling 3-month revenue per dept
    df.sort_values("date", inplace=True)
    return df

# ─────────────────────────────────────
# 6. VALIDATE
# ─────────────────────────────────────
def validate(df):
    print("\n=== Validation Report ===")
    print(f"Total records   : {len(df)}")
    print(f"Date range      : {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"Null values     : {df.isnull().sum().sum()}")
    print(f"Negative amounts: {(df['amount'] < 0).sum()}")
    print(f"Categories      : {df['category'].unique()}")
    print("✓ Validation passed!")

# ─────────────────────────────────────
# MAIN
# ─────────────────────────────────────
if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    df = detect_outliers(df)
    df = normalize(df)
    df = feature_engineering(df)
    validate(df)
    df.to_csv("data/processed_financial.csv", index=False)
    print("\nETL complete → data/processed_financial.csv")
