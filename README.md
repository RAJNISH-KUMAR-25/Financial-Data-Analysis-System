# Financial Data Analysis & Forecasting System

Analyzed 50,000+ financial records to evaluate revenue growth, expense trends, forecasting performance, and business insights.

## Tech Stack
`Python` `Pandas` `NumPy` `Scikit-learn` `SciPy` `Matplotlib` `Excel (openpyxl)` `SQL` `Power BI`

## Project Structure
```
├── data/
│   └── generate_data.py          # Generates 50K+ synthetic financial records
├── sql/
│   └── queries.sql               # KPI, budget variance, rolling revenue, outlier SQL
├── models/
│   └── forecasting.py            # Trend analysis + Revenue forecasting models
├── reports/
│   ├── generate_excel_report.py  # Multi-sheet Excel KPI workbook (4 sheets)
│   └── financial_dashboard.png   # Output dashboard image
├── etl_pipeline.py               # ETL: clean → outlier detection → normalize → feature engineering
├── dashboard.py                  # Matplotlib financial analytics dashboard
└── requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt

# Step 1 – Generate data
python data/generate_data.py

# Step 2 – Run ETL pipeline
python etl_pipeline.py

# Step 3 – Run forecasting models
python models/forecasting.py

# Step 4 – Generate Excel report
python reports/generate_excel_report.py

# Step 5 – View dashboard
python dashboard.py
```

## Key Features
- **ETL Pipeline** — Data cleaning, outlier detection (Z-Score + IQR), Min-Max & log normalization
- **Feature Engineering** — Budget variance, quarter/month flags, rolling averages
- **Trend Analysis** — Linear regression on monthly revenue with growth rate calculation
- **Revenue Forecasting** — Linear Regression & Gradient Boosting with MAE, RMSE, R² metrics
- **Excel Reports** — Monthly P&L, Department Budget, Forecast, Statistical Summary sheets
- **SQL Queries** — Rolling averages, budget utilization, outlier detection, growth rate queries
- **Dashboard** — KPI cards, Revenue vs Expense, Forecast with confidence interval, Donut chart
