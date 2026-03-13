import os
import pandas as pd

IN_PATH = os.path.join("data_raw", "Unemployment Rates.csv")
OUT_DIR = "data_processed"
OUT_PATH = os.path.join(OUT_DIR, "unemployment_quarterly.csv")

os.makedirs(OUT_DIR, exist_ok=True)

# Your file has 8 metadata lines, then 3 header lines, then data
raw = pd.read_csv(IN_PATH, skiprows=8, header=None)

# Drop the 3 header rows (they contain column labels/units)
raw = raw.iloc[3:].reset_index(drop=True)

# Keep the 6 columns we need (based on your file structure)
# 0 province, 1 gender, 2 age group, 3 month, 4 employment, 5 unemployment rate
raw = raw.iloc[:, :6]
raw.columns = ["province", "gender", "age_group", "month", "employment_k", "unemp_rate"]

# Fill down province/gender/age group (because they appear once then blanks)
raw[["province", "gender", "age_group"]] = raw[["province", "gender", "age_group"]].ffill()

# After ffill:
raw["province"] = raw["province"].astype(str).str.strip()

valid_provinces = {
    "Newfoundland and Labrador","Prince Edward Island","Nova Scotia","New Brunswick",
    "Quebec","Ontario","Manitoba","Saskatchewan","Alberta","British Columbia"
}

# Keep only real provinces
raw = raw[raw["province"].isin(valid_provinces)].copy()

# Keep Total gender only (drops Men+/Women+)
raw = raw[raw["gender"].astype(str).str.strip().eq("Total - Gender")]

# Keep 15+ only
raw = raw[raw["age_group"].astype(str).str.strip().eq("15 years and over")]

# Parse dates and numeric unemployment rate
raw["date"] = pd.to_datetime(raw["month"], errors="coerce")
raw["unemp_rate"] = pd.to_numeric(raw["unemp_rate"], errors="coerce")
raw = raw.dropna(subset=["province", "date", "unemp_rate"])

# Filter to your study window
start = pd.Timestamp("2016-01-01")
end = pd.Timestamp("2025-06-30")
raw = raw[(raw["date"] >= start) & (raw["date"] <= end)].copy()

# Quarter label
raw["qtr"] = raw["date"].dt.to_period("Q").astype(str)  # e.g., 2016Q1

# Monthly -> quarterly average unemployment by province
unemp_q = (
    raw.groupby(["province", "qtr"], as_index=False)
       .agg(unemp_q=("unemp_rate", "mean"))
       .sort_values(["province", "qtr"])
)


unemp_q.to_csv(OUT_PATH, index=False)
print(f"Saved: {OUT_PATH} ({len(unemp_q)} rows)")