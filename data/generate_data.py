import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

NUM_RECORDS = 50000
start_date = datetime(2020, 1, 1)

departments = ["Sales", "Marketing", "Operations", "HR", "IT", "Finance"]
categories  = ["Revenue", "Expense", "Investment", "Tax", "Refund"]
regions     = ["North", "South", "East", "West", "Central"]

data = pd.DataFrame({
    "record_id":    [f"FIN{str(i).zfill(6)}" for i in range(1, NUM_RECORDS + 1)],
    "date":         [(start_date + timedelta(days=random.randint(0, 1460))).strftime("%Y-%m-%d")
                     for _ in range(NUM_RECORDS)],
    "department":   np.random.choice(departments, NUM_RECORDS),
    "category":     np.random.choice(categories, NUM_RECORDS, p=[0.4, 0.35, 0.1, 0.1, 0.05]),
    "region":       np.random.choice(regions, NUM_RECORDS),
    "amount":       np.round(np.random.exponential(scale=5000, size=NUM_RECORDS) + 100, 2),
    "budget":       np.round(np.random.uniform(1000, 20000, NUM_RECORDS), 2),
    "approved":     np.random.choice([1, 0], NUM_RECORDS, p=[0.9, 0.1]),
})

# Inject some outliers
outlier_idx = np.random.choice(NUM_RECORDS, 200, replace=False)
data.loc[outlier_idx, "amount"] *= np.random.uniform(8, 15, 200)

data.to_csv("data/financial_records.csv", index=False)
print(f"Generated {len(data)} financial records → data/financial_records.csv")
