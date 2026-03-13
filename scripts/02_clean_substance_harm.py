import pandas as pd
import re
import os

IN_PATH = "data_raw/SubstanceHarmsData.csv"
OUT_PATH = "data_processed/opioid_outcomes_quarterly.csv"
os.makedirs("data_processed", exist_ok=True)

df = pd.read_csv(IN_PATH)

# 1) Filter
df = df[
    (df["Substance"] == "Opioids") &
    (df["Source"].isin(["Deaths", "Hospitalizations"])) &
    (df["Time_Period"] == "By quarter") &
    (df["Unit"] == "Number") &
    (df["Specific_Measure"] == "Overall numbers") &
    (df["Region"] != "Canada")
].copy()

# 2) Clean quarter format: "2016 Q1" -> "2016Q1"
df["qtr"] = df["Year_Quarter"].astype(str).str.replace(" ", "", regex=False)

# 3) Keep only 2016Q1–2025Q2
def qtr_to_index(q):
    m = re.match(r"^(\d{4})Q([1-4])$", q)
    if not m:
        return None
    y, qq = int(m.group(1)), int(m.group(2))
    return y * 4 + qq

df["qtr_idx"] = df["qtr"].apply(qtr_to_index)
df = df[df["qtr_idx"].between(qtr_to_index("2016Q1"), qtr_to_index("2025Q2"))]

# 4) Pivot wide: deaths + hosp
wide = (
    df.pivot_table(index=["Region", "qtr"], columns="Source", values="Value", aggfunc="sum")
      .reset_index()
      .rename(columns={"Region": "province", "Deaths": "deaths", "Hospitalizations": "hosp"})
)

# 5) Save
wide = wide.sort_values(["province", "qtr"])
wide.to_csv(OUT_PATH, index=False)
print(f"Saved: {OUT_PATH} ({len(wide)} rows)")