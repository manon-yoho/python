
import numpy as np
import pandas as pd



mock_data = {
    "employee_id": [
        101,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
    ],
    "department": [
        "Sales",
        "Engineering",
        "HR",
        "Sales",
        "Finance",
        "Engineering",
        "HR",
        "Sales",
        "Finance",
        "Engineering",
    ],
    "salary": [
        50000,
        65000,
        45000,
        55000,
        60000,
        70000,
        48000,
        62000,
        52000,
        52000,
    ],
}
df = pd.DataFrame(mock_data)
df.to_csv("raw_data.csv", index=False)


df = pd.read_csv("raw_data.csv")



before_rows = len(df)
before_missing = int(df.isna().sum().sum())
before_duplicates = int(df.duplicated().sum())

print(
    f"Before -> Rows: {before_rows}, Missing: {before_missing},"
    f" Duplicates: {before_duplicates}"
)


df = df.dropna(subset=["employee_id"])  # Reason: cannot identify record without ID

# - Fill numeric columns with median (robust to skewness/outliers)
if "salary" in df.columns:
  df["salary"] = df["salary"].fillna(
      df["salary"].median()
  )  # Reason: skewed salary distribution

# - Fill categorical columns with mode or a flag
if "department" in df.columns:
  df["department"] = df["department"].fillna(
      df["department"].mode()[0]
  )  # Reason: most frequent category

# - Leave & flag if missingness itself may carry signal
if "performance_score" in df.columns:
  df["performance_score_missing"] = df["performance_score"].isna().astype(int)
  # Dates
if "hire_date" in df.columns:
  df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")

# Numbers stored as text (e.g., "$50,000" or "1200")
for col in ["salary", "age", "tenure_years"]:
  if col in df.columns and df[col].dtype == "object":
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(r"[$,]", "", regex=True).str.strip(),
        errors="coerce",
    )

# Categories
for col in ["department", "city", "gender", "contract_type"]:
  if col in df.columns:
    df[col] = df[col].astype("category")
    # Remove exact duplicate rows
df = df.drop_duplicates()

# Standardise string columns (strip whitespace + consistent casing)
text_cols = df.select_dtypes(include=["object", "string"]).columns
for col in text_cols:
  df[col] = df[col].str.strip().str.title()  # use .str.lower() if preferred



def detect_outliers_iqr(series):
  q1 = series.quantile(0.25)
  q3 = series.quantile(0.75)
  iqr = q3 - q1
  lower = q1 - 1.5 * iqr
  upper = q3 + 1.5 * iqr
  mask = (series < lower) | (series > upper)
  return mask, lower, upper


# Example on a numeric column
num_col = "salary"  # replace with your numeric column
if num_col in df.columns:
  outlier_mask, low, high = detect_outliers_iqr(df[num_col].dropna())
  print(
      f"Outliers in {num_col}: {outlier_mask.sum()} (bounds: {low:.2f} to"
      f" {high:.2f})"
  )




  after_rows = len(df)
after_missing = int(df.isna().sum().sum())
after_duplicates = int(df.duplicated().sum())

summary_df = pd.DataFrame({
    "Metric": ["Rows", "Missing Values", "Duplicate Rows"],
    "Before": [before_rows, before_missing, before_duplicates],
    "After": [after_rows, after_missing, after_duplicates],
})

print("\nBefore / After Cleaning Summary:")
print(summary_df.to_string(index=False))

# Save cleaned dataset
df.to_csv("clean_data.csv", index=False)


