import pandas as pd
from pathlib import Path

# =========================
# PROJECT PATH SETUP
# =========================
project_root = Path(__file__).resolve().parent.parent

raw_path = project_root / "data" / "raw"
processed_path = project_root / "data" / "processed"

processed_path.mkdir(parents=True, exist_ok=True)

# =========================
# 1. CLEAN NAV HISTORY
# =========================
nav = pd.read_csv(raw_path / "02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"], errors="coerce")
nav["nav"] = pd.to_numeric(nav["nav"], errors="coerce")

# Remove invalid NAV
nav = nav[nav["nav"] > 0]

# Remove duplicates
nav = nav.drop_duplicates(subset=["amfi_code", "date"])

# Sort
nav = nav.sort_values(["amfi_code", "date"])

# Forward fill NAV per fund
nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

# Save
nav.to_csv(processed_path / "nav_history_cleaned.csv", index=False)


# =========================
# 2. CLEAN INVESTOR TRANSACTIONS
# =========================
txn = pd.read_csv(raw_path / "08_investor_transactions.csv")

# Standardize transaction types
txn["transaction_type"] = txn["transaction_type"].str.upper().str.strip()

txn["transaction_type"] = txn["transaction_type"].replace({
    "SIP": "SIP",
    "SYSTEMATIC": "SIP",
    "LUMPSUM": "LUMPSUM",
    "REDEMPTION": "REDEMPTION",
    "REDEEM": "REDEMPTION"
})

# Fix date
txn["date"] = pd.to_datetime(txn["date"], errors="coerce")

# Validate amount
txn["amount"] = pd.to_numeric(txn["amount"], errors="coerce")
txn = txn[txn["amount"] > 0]

# KYC validation (keep only valid values)
valid_kyc = ["VERIFIED", "PENDING", "REJECTED"]
txn["kyc_status"] = txn["kyc_status"].str.upper().str.strip()
txn = txn[txn["kyc_status"].isin(valid_kyc)]

# Save
txn.to_csv(processed_path / "investor_transactions_cleaned.csv", index=False)


# =========================
# 3. CLEAN SCHEME PERFORMANCE
# =========================
perf = pd.read_csv(raw_path / "07_scheme_performance.csv")

# Convert numeric columns
numeric_cols = perf.columns.drop(["amfi_code"])
for col in numeric_cols:
    perf[col] = pd.to_numeric(perf[col], errors="coerce")

# Remove rows with missing critical values
perf = perf.dropna(subset=numeric_cols)

# Expense ratio validation (0.1% to 2.5%)
if "expense_ratio" in perf.columns:
    perf = perf[(perf["expense_ratio"] >= 0.1) & (perf["expense_ratio"] <= 2.5)]

# Flag anomalies (basic rule: extreme returns)
for col in numeric_cols:
    if "return" in col.lower():
        perf = perf[(perf[col] > -100) & (perf[col] < 500)]

# Save
perf.to_csv(processed_path / "scheme_performance_cleaned.csv", index=False)


# =========================
# DONE MESSAGE
# =========================
print("\nCLEANING COMPLETE")
print("Files saved in:", processed_path)