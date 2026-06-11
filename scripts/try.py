import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

raw_path = project_root / "data" / "raw"

df = pd.read_csv(raw_path /"04_monthly_sip_inflows.csv")
print(df.head())