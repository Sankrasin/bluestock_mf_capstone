import requests
import pandas as pd
from pathlib import Path

print("\n" + "=" * 60)
print("FETCHING HDFC TOP 100 DIRECT NAV DATA")
print("=" * 60)

# AMFI Code for HDFC Top 100 Direct
scheme_code = 125497

# API URL
url = f"https://api.mfapi.in/mf/{scheme_code}"

try:

    # Fetch data from API
    response = requests.get(url)

    if response.status_code == 200:

        # Parse JSON response
        data = response.json()

        # Extract metadata
        meta = data["meta"]

        # Extract NAV history
        nav_df = pd.DataFrame(data["data"])

        # Add metadata columns to every NAV record
        nav_df["fund_house"] = meta.get("fund_house")
        nav_df["scheme_type"] = meta.get("scheme_type")
        nav_df["scheme_category"] = meta.get("scheme_category")
        nav_df["scheme_code"] = meta.get("scheme_code")
        nav_df["scheme_name"] = meta.get("scheme_name")
        nav_df["isin_growth"] = meta.get("isin_growth")
        nav_df["isin_div_reinvestment"] = meta.get("isin_div_reinvestment")

        # Create raw data folder
        raw_folder = Path(__file__).resolve().parent.parent
        raw_folder = raw_folder / "data" / "raw"
        raw_folder.mkdir(parents=True, exist_ok=True)

        # Output file
        output_file = raw_folder / "HDFC_Top100_Direct_nav.csv"

        # Save CSV
        nav_df.to_csv(output_file, index=False)

        print("\nCSV Saved Successfully")
        print("Location:", output_file)
        print(nav_df)

    else:

        print("Failed to fetch data")
        print("Status Code:", response.status_code)

except Exception as e:

    print("Error:", e)