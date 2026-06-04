-- 1. Top 5 funds by AUM
SELECT fund_house, SUM(aum_crore) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT d.year, d.month, AVG(f.nav) AS avg_nav
FROM fact_nav f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. Monthly SIP inflow trend
SELECT d.year, d.month, SUM(ft.amount_inr) AS sip_inflow
FROM fact_transactions ft
JOIN dim_date d ON ft.date_id = d.date_id
WHERE ft.transaction_type = 'SIP'
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 4. Transactions by state
SELECT state, COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- 5. Funds with expense ratio < 1%
SELECT amfi_code, expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1;

-- 6. Top 5 performing funds (3Y return)
SELECT amfi_code, return_3yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- 7. Risk vs return (average)
SELECT amfi_code,
       AVG(return_3yr_pct) AS avg_return,
       AVG(sharpe_ratio) AS avg_sharpe
FROM fact_performance
GROUP BY amfi_code;

-- 8. Transaction type distribution
SELECT transaction_type, COUNT(*) AS count
FROM fact_transactions
GROUP BY transaction_type;

-- 9. SIP inflow by state
SELECT state, SUM(amount_inr) AS sip_total
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY state
ORDER BY sip_total DESC;

-- 10. NAV volatility per fund
SELECT amfi_code,
       MAX(nav) - MIN(nav) AS nav_volatility
FROM fact_nav
GROUP BY amfi_code;