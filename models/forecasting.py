import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────
# 1. TREND ANALYSIS
# ─────────────────────────────────────
def trend_analysis(df):
    print("=== Trend Analysis ===")

    monthly = df[df["category"] == "Revenue"].groupby("month_str")["amount"].sum().reset_index()
    monthly.columns = ["month", "revenue"]
    monthly["month_idx"] = range(len(monthly))

    # Linear trend
    X = monthly[["month_idx"]]
    y = monthly["revenue"]
    model = LinearRegression().fit(X, y)
    monthly["trend"] = model.predict(X)

    slope = model.coef_[0]
    trend_dir = "Upward ↑" if slope > 0 else "Downward ↓"
    print(f"Revenue trend   : {trend_dir}")
    print(f"Monthly growth  : ${slope:,.2f} per month")
    print(f"R² Score        : {r2_score(y, monthly['trend']):.4f}")

    monthly.to_csv("data/trend_analysis.csv", index=False)
    print("Saved → data/trend_analysis.csv\n")
    return monthly, model

# ─────────────────────────────────────
# 2. REVENUE FORECASTING
# ─────────────────────────────────────
def revenue_forecast(df):
    print("=== Revenue Forecasting ===")

    revenue_df = df[df["category"] == "Revenue"].copy()
    features = ["year", "month", "quarter", "day_of_week",
                "budget", "amount_log", "over_budget"]
    features = [f for f in features if f in revenue_df.columns]

    X = revenue_df[features].fillna(0)
    y = revenue_df["amount"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train_s, y_train)
    lr_pred = lr.predict(X_test_s)

    # Gradient Boosting
    gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    gb_pred = gb.predict(X_test)

    print(f"{'Model':<25} {'MAE':>10} {'RMSE':>12} {'R²':>8}")
    print("-" * 58)
    for name, pred in [("Linear Regression", lr_pred), ("Gradient Boosting", gb_pred)]:
        mae  = mean_absolute_error(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        r2   = r2_score(y_test, pred)
        print(f"{name:<25} ${mae:>9,.2f} ${rmse:>11,.2f} {r2:>8.4f}")

    # Next 6 months forecast
    last = X_test.iloc[-1:].copy()
    forecast = []
    for i in range(1, 7):
        last["month"] = (last["month"].values[0] % 12) + 1
        pred_val = gb.predict(last)[0]
        forecast.append({"month_offset": i, "forecasted_revenue": round(pred_val, 2)})

    forecast_df = pd.DataFrame(forecast)
    forecast_df.to_csv("data/forecast.csv", index=False)
    print("\nNext 6-Month Forecast:")
    print(forecast_df.to_string(index=False))
    print("Saved → data/forecast.csv\n")
    return gb

# ─────────────────────────────────────
# 3. STATISTICAL SUMMARY
# ─────────────────────────────────────
def statistical_summary(df):
    print("=== Statistical Summary ===")
    stats = df.groupby("category")["amount"].agg(
        count="count", mean="mean", median="median",
        std="std", min="min", max="max",
        total="sum"
    ).round(2)
    print(stats)
    stats.to_csv("data/statistical_summary.csv")
    print("Saved → data/statistical_summary.csv\n")

# ─────────────────────────────────────
# MAIN
# ─────────────────────────────────────
if __name__ == "__main__":
    df = pd.read_csv("data/processed_financial.csv")
    statistical_summary(df)
    trend_analysis(df)
    revenue_forecast(df)
