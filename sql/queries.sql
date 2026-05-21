-- ============================================
-- Financial Data Analysis System - SQL Queries
-- ============================================

CREATE TABLE financial_records (
    record_id      VARCHAR(10) PRIMARY KEY,
    date           DATE,
    department     VARCHAR(30),
    category       VARCHAR(20),
    region         VARCHAR(20),
    amount         DECIMAL(12,2),
    budget         DECIMAL(12,2),
    approved       TINYINT
);

-- ============================================
-- KPI QUERIES
-- ============================================

-- 1. Monthly Revenue vs Expense Summary
SELECT
    DATE_FORMAT(date, '%Y-%m')      AS month,
    SUM(CASE WHEN category = 'Revenue' THEN amount ELSE 0 END) AS total_revenue,
    SUM(CASE WHEN category = 'Expense' THEN amount ELSE 0 END) AS total_expense,
    SUM(CASE WHEN category = 'Revenue' THEN amount ELSE 0 END) -
    SUM(CASE WHEN category = 'Expense' THEN amount ELSE 0 END) AS net_profit
FROM financial_records
GROUP BY month
ORDER BY month;

-- 2. Department Budget vs Actual Spend
SELECT
    department,
    SUM(budget)                         AS total_budget,
    SUM(amount)                         AS total_actual,
    SUM(amount - budget)                AS variance,
    ROUND(100 * SUM(amount) / SUM(budget), 2) AS utilization_pct
FROM financial_records
WHERE category = 'Expense'
GROUP BY department
ORDER BY variance DESC;

-- 3. Revenue Growth Rate by Quarter
SELECT
    year,
    quarter,
    SUM(amount) AS quarterly_revenue,
    LAG(SUM(amount)) OVER (ORDER BY year, quarter) AS prev_quarter,
    ROUND(100 * (SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY year, quarter))
          / NULLIF(LAG(SUM(amount)) OVER (ORDER BY year, quarter), 0), 2) AS growth_pct
FROM (
    SELECT YEAR(date) AS year, QUARTER(date) AS quarter, amount
    FROM financial_records WHERE category = 'Revenue'
) q
GROUP BY year, quarter;

-- 4. Top Expense Categories by Region
SELECT
    region,
    category,
    COUNT(*)        AS transactions,
    SUM(amount)     AS total_amount,
    AVG(amount)     AS avg_amount
FROM financial_records
WHERE category = 'Expense'
GROUP BY region, category
ORDER BY region, total_amount DESC;

-- 5. Outlier Detection — Amounts > 3x Department Average
SELECT
    r.record_id, r.department, r.category, r.amount, dept_avg.avg_amount,
    ROUND(r.amount / dept_avg.avg_amount, 2) AS amount_ratio
FROM financial_records r
JOIN (
    SELECT department, AVG(amount) AS avg_amount
    FROM financial_records GROUP BY department
) dept_avg ON r.department = dept_avg.department
WHERE r.amount > 3 * dept_avg.avg_amount
ORDER BY amount_ratio DESC;

-- 6. Unapproved High-Value Transactions
SELECT record_id, date, department, category, amount
FROM financial_records
WHERE approved = 0 AND amount > 10000
ORDER BY amount DESC;

-- 7. Rolling 3-Month Revenue
SELECT
    date,
    amount,
    AVG(amount) OVER (
        ORDER BY date
        ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
    ) AS rolling_3m_avg
FROM financial_records
WHERE category = 'Revenue'
ORDER BY date;

-- Indexes for performance
CREATE INDEX idx_fin_date       ON financial_records(date);
CREATE INDEX idx_fin_category   ON financial_records(category);
CREATE INDEX idx_fin_department ON financial_records(department);
