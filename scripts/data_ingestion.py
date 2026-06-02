from pathlib import Path
import pandas as pd

# Get project root folder
project_folder = Path(__file__).resolve().parent.parent

# Path to raw data folder
raw_folder = project_folder / "data" / "raw"

# Get all csv files
csv_files = list(raw_folder.glob("*.csv"))

print("\nStarting data ingestion...\n")

print("Files found:", len(csv_files))

for file in csv_files:

    print("-" * 60)
    print("Reading:", file.name)

    try:
        df = pd.read_csv(file)

        # Number of rows and columns
        print("\nShape:")
        print(df.shape)

        # Column data types
        print("\nData Types:")
        print(df.dtypes)

        # First 5 records
        print("\nHead:")
        print(df.head())

        # Check missing values
        print("\nMissing Values:")
        print(df.isnull().sum())

    except Exception as e:
        print("Error:", e)

    print("-" * 60)

print("\n")

print("=" * 60)

print("AMFI CODE VALIDATION")

print("=" * 60)

# Read required files

fund_master = pd.read_csv(raw_folder / "01_fund_master.csv")

nav_history = pd.read_csv(raw_folder / "02_nav_history.csv")

# Get unique AMFI codes

fund_codes = set(fund_master["amfi_code"])

nav_codes = set(nav_history["amfi_code"])

# Find codes present in fund master but missing in NAV history

missing_codes = fund_codes - nav_codes

print("Fund Master Codes:", len(fund_codes))

print("NAV History Codes:", len(nav_codes))

if len(missing_codes) == 0:

    print("\nAll AMFI codes are present in NAV history.")

else:

    print("\nMissing AMFI Codes:")

    print(missing_codes)

print("\n")
print("=" * 60)
print("FUND MASTER ANALYSIS")
print("=" * 60)

# Fund houses
fund_houses = sorted(set(fund_master["fund_house"]))
print("\nFund Houses:")
print(fund_houses)
print("Count:", len(fund_houses))

# Categories
categories = sorted(set(fund_master["category"]))
print("\nCategories:")
print(categories)
print("Count:", len(categories))

# Sub categories
sub_categories = sorted(set(fund_master["sub_category"]))
print("\nSub Categories:")
print(sub_categories)
print("Count:", len(sub_categories))

# Risk categories
risk_categories = sorted(set(fund_master["risk_category"]))
print("\nRisk Categories:")
print(risk_categories)
print("Count:", len(risk_categories))