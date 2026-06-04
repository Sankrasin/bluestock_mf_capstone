# Bluestock Mutual Fund Analytics — Data Dictionary

---

# 1. DIMENSION TABLES

---

## dim_fund (Fund Master Dimension)

Purpose: Stores static metadata about mutual funds.

Columns:

amfi_code (INTEGER): Unique AMFI identifier for each mutual fund scheme (Primary key reference)  
fund_house (TEXT): Asset Management Company managing the fund  
category (TEXT): Fund category (Equity / Debt)  
sub_category (TEXT): Sub category like Large Cap, Mid Cap, Liquid, etc.  
risk_category (TEXT): Risk level of fund (Low / Moderate / High / Very High)

---

## dim_date (Date Dimension)

Purpose: Standard calendar table for time-series analysis.

Columns:

date_id (INTEGER): Surrogate key for date (Primary Key)  
full_date (DATE): Actual calendar date  
year (INTEGER): Year extracted from date  
month (INTEGER): Month (1–12)  
day (INTEGER): Day of month  
quarter (INTEGER): Quarter (1–4)

---

# 2. FACT TABLES

---

## fact_nav (NAV Fact Table)

Purpose: Stores daily Net Asset Value of funds.

Columns:

amfi_code (INTEGER): Foreign key to dim_fund  
date_id (INTEGER): Foreign key to dim_date  
nav (REAL): Net Asset Value of fund on given date

Business Use:
- NAV trend analysis  
- Fund performance tracking  
- Volatility analysis  

---

## fact_transactions (Investor Transactions Fact)

Purpose: Stores investor transaction data.

Columns:

investor_id (TEXT): Unique investor identifier  
amfi_code (INTEGER): Fund identifier  
date_id (INTEGER): Transaction date reference  
transaction_type (TEXT): SIP / Lumpsum / Redemption  
amount_inr (REAL): Transaction amount in INR  
state (TEXT): Investor state  
city (TEXT): Investor city  
kyc_status (TEXT): KYC status (Verified / Pending / Rejected)

Business Use:
- Investor behavior analysis  
- SIP vs redemption trends  
- Geographic distribution analysis  

---

## fact_performance (Fund Performance Fact)

Purpose: Stores fund performance metrics.

Columns:

amfi_code (INTEGER): Fund identifier  
return_1yr_pct (REAL): 1-year return (%)  
return_3yr_pct (REAL): 3-year return (%)  
return_5yr_pct (REAL): 5-year return (%)  
expense_ratio_pct (REAL): Expense ratio (%)  
alpha (REAL): Excess return over benchmark  
beta (REAL): Market sensitivity  
sharpe_ratio (REAL): Risk-adjusted return  
sortino_ratio (REAL): Downside risk-adjusted return  

Business Use:
- Fund ranking  
- Risk analysis  
- Portfolio optimization  

---

## fact_aum (Assets Under Management Fact)

Purpose: Tracks fund house AUM over time.

Columns:

fund_house (TEXT): AMC name  
date_id (INTEGER): Date reference  
aum_lakh_crore (REAL): AUM in lakh crore  
aum_crore (INTEGER): AUM in crore  
num_schemes (INTEGER): Number of schemes

Business Use:
- AMC comparison  
- Market share tracking  
- Growth analysis  

---

# 3. ETL PIPELINE

Raw CSV → Cleaning (Pandas) → Processed CSV → SQLite Star Schema → SQL Analytics → Insights

---

# 4. DATABASE DESIGN

Star Schema:

Dimensions:
- dim_fund
- dim_date

Facts:
- fact_nav
- fact_transactions
- fact_performance
- fact_aum

---

# 5. KEY BUSINESS TERMS

NAV: Net Asset Value per unit of mutual fund  
AUM: Total assets managed by fund house  
SIP: Systematic Investment Plan  
Expense Ratio: Annual fund management fee  
Alpha: Excess return over benchmark  
Beta: Market sensitivity  
Sharpe Ratio: Risk-adjusted return  
Sortino Ratio: Downside risk-adjusted return  

---

# 6. DATA SOURCES

fund_master: AMFI dataset  
nav_history: MF API + project dataset  
investor_transactions: Project dataset  
scheme_performance: AMFI analytics dataset  
aum_by_fund_house: Industry dataset  
benchmark_indices: Market index dataset  

---