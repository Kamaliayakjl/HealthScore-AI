import pandas as pd

# 1. Load the original dataset
df = pd.read_csv("final_data.csv")

print("ORIGINAL DATASET")
print("Rows and columns:", df.shape)
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

# 2. Confirm the dataset is large enough
if len(df) < 1500:
    raise ValueError("The dataset contains fewer than 1,500 rows.")

# 3. Randomly select 1,500 rows
sample = df.sample(n=1500, random_state=42)

# 4. Save the sample separately
sample.to_csv("healthscore_1500.csv", index=False)

print("\nSAMPLE DATASET")
print("Rows and columns:", sample.shape)
print("Missing values:", sample.isnull().sum().sum())
print("Duplicate rows:", sample.duplicated().sum())

# 5. Compare the five target-score distributions
targets = [
    "diabetes_risk_score",
    "hypertension_risk_score",
    "heart_disease_risk_score",
    "obesity_risk_score",
    "cholesterol_risk_score"
]

print("\nTARGET SCORE COMPARISON")
for column in targets:
    if column not in df.columns:
        print(f"Missing target column: {column}")
        continue

    print(f"\n{column}")
    print("Original:")
    print(df[column].describe().round(2))
    print("Sample:")
    print(sample[column].describe().round(2))

print("\nSampling and initial validation completed.")
