import pandas as pd
import sqlite3
from pathlib import Path

# =========================
# PROJECT ROOT (SAFE FIX)
# =========================
project_root = Path(__file__).resolve().parent.parent

raw_path = project_root / "data" / "raw"
processed_path = project_root / "data" / "processed"
db_path = project_root / "data" / "db" / "bluestock_mf.db"
sql_path = project_root / "sql" / "schema.sql"

db_path.parent.mkdir(parents=True, exist_ok=True)

# =========================
# CONNECT SQLITE
# =========================
conn = sqlite3.connect(db_path)

print("DB created at:", db_path)

# =========================
# RUN SCHEMA
# =========================
with open(sql_path, "r") as f:
    conn.executescript(f.read())

print("Schema executed successfully")

# =========================
# LOAD DATASETS
# =========================
nav = pd.read_csv(processed_path / "nav_history_cleaned.csv")
txn = pd.read_csv(processed_path / "investor_transactions_cleaned.csv")
perf = pd.read_csv(processed_path / "scheme_performance_cleaned.csv")
aum = pd.read_csv(raw_path / "03_aum_by_fund_house.csv")
fund = pd.read_csv(raw_path / "01_fund_master.csv")

# =========================
# DIM_FUND
# =========================
dim_fund = fund[[
    "amfi_code",
    "fund_house",
    "category",
    "sub_category",
    "risk_category"
]].drop_duplicates()

dim_fund.to_sql("dim_fund", conn, if_exists="replace", index=False)

# =========================
# DIM_DATE (FIXED - WITH date_id)
# =========================
nav["date"] = pd.to_datetime(nav["date"])

dim_date = pd.DataFrame()
dim_date["full_date"] = nav["date"].drop_duplicates()
dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])

dim_date = dim_date.sort_values("full_date").reset_index(drop=True)

# IMPORTANT FIX: create date_id
dim_date["date_id"] = dim_date.index + 1

dim_date["year"] = dim_date["full_date"].dt.year
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["day"] = dim_date["full_date"].dt.day
dim_date["quarter"] = dim_date["full_date"].dt.quarter

dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)

# reload from DB
dim_date_db = pd.read_sql("SELECT * FROM dim_date", conn)
dim_date_db["full_date"] = pd.to_datetime(dim_date_db["full_date"])

# =========================
# FACT_NAV
# =========================
nav["date"] = pd.to_datetime(nav["date"])

nav = nav.merge(
    dim_date_db,
    left_on="date",
    right_on="full_date",
    how="left"
)

fact_nav = nav[["amfi_code", "date_id", "nav"]]
fact_nav.to_sql("fact_nav", conn, if_exists="replace", index=False)

# =========================
# FACT_TRANSACTIONS
# =========================
txn_date_col = [c for c in txn.columns if "date" in c][0]
txn[txn_date_col] = pd.to_datetime(txn[txn_date_col])

txn = txn.merge(
    dim_date_db,
    left_on=txn_date_col,
    right_on="full_date",
    how="left"
)

fact_txn = txn[[
    "investor_id",
    "amfi_code",
    "date_id",
    "transaction_type",
    "amount_inr",
    "state",
    "city",
    "kyc_status"
]]

fact_txn.to_sql("fact_transactions", conn, if_exists="replace", index=False)

# =========================
# FACT_PERFORMANCE
# =========================
fact_perf = perf[[
    "amfi_code",
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "expense_ratio_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio"
]]

fact_perf.to_sql("fact_performance", conn, if_exists="replace", index=False)

# =========================
# FACT_AUM
# =========================
aum["date"] = pd.to_datetime(aum["date"])

aum = aum.merge(
    dim_date_db,
    left_on="date",
    right_on="full_date",
    how="left"
)

fact_aum = aum[[
    "fund_house",
    "date_id",
    "aum_lakh_crore",
    "aum_crore",
    "num_schemes"
]]

fact_aum.to_sql("fact_aum", conn, if_exists="replace", index=False)

# =========================
# VALIDATION CHECK
# =========================
print("\nROW COUNT CHECK:")

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

for t in tables:
    count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {count}")

conn.close()

print("\nPIPELINE COMPLETED SUCCESSFULLY ")