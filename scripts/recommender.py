import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

scorecard = pd.read_csv(
    project_root / "reports" / "fund_scorecard.csv"
)

fund_master = pd.read_csv(
    project_root / "data/raw/01_fund_master.csv"
)

recommender_df = scorecard.merge(
    fund_master[
        ["amfi_code", "risk_category"]
    ],
    on="amfi_code",
    how="left"
)

risk_input = input(
    "Enter risk appetite (Low / Moderate / High): "
).strip()

risk_map = {
    "Low": ["Low"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"]
}

if risk_input not in risk_map:
    print("Invalid risk appetite.")
else:

    recommendations = (
        recommender_df[
            recommender_df["risk_category"]
            .isin(risk_map[risk_input])
        ]
        .sort_values(
            "sharpe_ratio",
            ascending=False
        )
        .head(3)
    )

    print("\nTop 3 Recommended Funds\n")

    print(
        recommendations[
            [
                "scheme_name",
                "risk_category",
                "sharpe_ratio"
            ]
        ]
    )