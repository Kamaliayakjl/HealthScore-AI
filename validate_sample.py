import pandas as pd

# Load both datasets
original = pd.read_csv("final_data.csv")
sample = pd.read_csv("healthscore_1500.csv")

print("Original shape:", original.shape)
print("Sample shape:", sample.shape)

# Check required target columns
targets = [
    "diabetes_risk_score",
    "hypertension_risk_score",
    "heart_disease_risk_score",
    "obesity_risk_score",
    "cholesterol_risk_score"
]

missing_targets = [c for c in targets if c not in original.columns]

if missing_targets:
    raise ValueError(f"Target columns not found: {missing_targets}")

# 1. Compare target-score distributions
target_results = []

for col in targets:
    for dataset_name, data in [
        ("Original", original),
        ("Sample", sample)
    ]:
        s = data[col]

        target_results.append({
            "Target": col,
            "Dataset": dataset_name,
            "Count": s.count(),
            "Mean": s.mean(),
            "Std": s.std(),
            "Min": s.min(),
            "25%": s.quantile(0.25),
            "Median": s.median(),
            "75%": s.quantile(0.75),
            "Max": s.max()
        })

target_report = pd.DataFrame(target_results)
target_report.to_csv("target_validation.csv", index=False)

print("\nTARGET SCORE COMPARISON")
print(target_report.round(2).to_string(index=False))

# 2. Compare categorical proportions
categorical_cols = original.select_dtypes(
    include=["object", "category", "bool"]
).columns

category_results = []

for col in categorical_cols:
    original_pct = original[col].value_counts(
        normalize=True, dropna=False
    ) * 100

    sample_pct = sample[col].value_counts(
        normalize=True, dropna=False
    ) * 100

    comparison = pd.concat(
        [
            original_pct.rename("Original_Percent"),
            sample_pct.rename("Sample_Percent")
        ],
        axis=1
    ).fillna(0)

    comparison["Difference_Percentage_Points"] = (
        comparison["Sample_Percent"]
        - comparison["Original_Percent"]
    )

    for category, row in comparison.iterrows():
        category_results.append({
            "Column": col,
            "Category": str(category),
            "Original_Percent": row["Original_Percent"],
            "Sample_Percent": row["Sample_Percent"],
            "Difference_Percentage_Points":
                row["Difference_Percentage_Points"]
        })

category_report = pd.DataFrame(category_results)
category_report.to_csv("category_validation.csv", index=False)

print("\nCategorical comparison saved.")
print("Largest category proportion differences:")
if not category_report.empty:
    print(
        category_report.assign(
            Abs_Difference=category_report[
                "Difference_Percentage_Points"
            ].abs()
        ).sort_values(
            "Abs_Difference", ascending=False
        ).head(15).round(2).to_string(index=False)
    )

# 3. Compare numerical feature distributions
numeric_cols = original.select_dtypes(include="number").columns

numeric_results = []

for col in numeric_cols:
    for dataset_name, data in [
        ("Original", original),
        ("Sample", sample)
    ]:
        s = data[col]

        numeric_results.append({
            "Feature": col,
            "Dataset": dataset_name,
            "Count": s.count(),
            "Mean": s.mean(),
            "Std": s.std(),
            "Min": s.min(),
            "25%": s.quantile(0.25),
            "Median": s.median(),
            "75%": s.quantile(0.75),
            "Max": s.max()
        })

numeric_report = pd.DataFrame(numeric_results)
numeric_report.to_csv("numeric_validation.csv", index=False)

print("\nNumerical comparison saved.")
print("\nVALIDATION REPORTS CREATED:")
print("1. target_validation.csv")
print("2. category_validation.csv")
print("3. numeric_validation.csv")
print("\nReview completed. Sampling is not yet approved.")

