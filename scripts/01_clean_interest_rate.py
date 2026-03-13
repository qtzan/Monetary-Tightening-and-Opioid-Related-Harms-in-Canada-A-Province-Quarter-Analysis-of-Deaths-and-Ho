import os
import pandas as pd

IN_PATH = os.path.join("data_raw", "Interest Rates.csv")
OUT_DIR = "data_processed"
OUT_PATH = os.path.join(OUT_DIR, "rate_quarterly.csv")

os.makedirs(OUT_DIR, exist_ok=True)

# Line 8 (1-indexed) contains the header: date, V39079
# => skip first 7 lines
df = pd.read_csv(IN_PATH, skiprows=8)

# Standardize column names
df.columns = [c.strip() for c in df.columns]

if "date" not in df.columns:
    raise ValueError(f"Expected a 'date' column after skipping 7 rows. Columns: {df.columns.tolist()}")

# The rate column is V39079 (or second column if named differently)
rate_col = "V39079" if "V39079" in df.columns else df.columns[1]
df = df.rename(columns={rate_col: "rate"})

# Clean types
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
df = df.dropna(subset=["date", "rate"]).sort_values("date")

# Filter to 2016Q1–2025Q2 window
start = pd.Timestamp("2016-01-01")
end = pd.Timestamp("2025-06-30")
df = df[(df["date"] >= start) & (df["date"] <= end)].copy()

# Quarter label
df["qtr"] = df["date"].dt.to_period("Q").astype(str)  # e.g., 2016Q1

# Quarterly aggregation
quarterly = (
    df.groupby("qtr", as_index=False)
      .agg(avg_rate_q=("rate", "mean"),
           end_date_q=("date", "max"))
)

# End-of-quarter rate
end_rates = (
    df.loc[df.groupby("qtr")["date"].idxmax(), ["qtr", "rate"]]
      .rename(columns={"rate": "end_rate_q"})
)

quarterly = quarterly.merge(end_rates, on="qtr", how="left").sort_values("end_date_q")

# Shocks + lags
quarterly["shock_bp_q"] = quarterly["end_rate_q"].diff()
quarterly["shock_50bp_q"] = (quarterly["shock_bp_q"] >= 0.50).astype("int64")
quarterly["shock_50bp_lag1"] = quarterly["shock_50bp_q"].shift(1)
quarterly["shock_50bp_lag2"] = quarterly["shock_50bp_q"].shift(2)



out = quarterly[[
    "qtr", "avg_rate_q", "end_rate_q", "shock_bp_q",
    "shock_50bp_q", "shock_50bp_lag1", "shock_50bp_lag2"
]].copy()


out.to_csv(OUT_PATH, index=False)
print(f"Saved cleaned quarterly interest rate data to: {OUT_PATH} ({len(out)} quarters)")