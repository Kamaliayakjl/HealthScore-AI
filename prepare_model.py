# HealthScore AI - Complete Machine Learning Pipeline

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# --------------------------------------------------
# 1. LOAD DATASET
# --------------------------------------------------

print("=" * 60)
print("       HEALTHSCORE AI - MACHINE LEARNING")
print("=" * 60)

DATA_FILE = "healthscore_1500.csv"

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(
        f"{DATA_FILE} not found. Keep this Python file "
        "in the same folder as your CSV dataset."
    )

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully!")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])


# --------------------------------------------------
# 2. DEFINE TARGET COLUMNS
# --------------------------------------------------

targets = [
    "diabetes_risk_score",
    "hypertension_risk_score",
    "heart_disease_risk_score",
    "obesity_risk_score",
    "cholesterol_risk_score"
]

missing_targets = [col for col in targets if col not in df.columns]

if missing_targets:
    raise ValueError(
        f"The following target columns are missing: {missing_targets}"
    )

# Convert target columns to numeric values.
for col in targets:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows where any target score is missing or invalid.
df = df.dropna(subset=targets).copy()

if len(df) < 10:
    raise ValueError(
        "Not enough valid rows to train and test the model."
    )

print("Rows available for modelling:", len(df))
print("Number of target scores:", len(targets))


# --------------------------------------------------
# 3. SEPARATE INPUT FEATURES AND TARGETS
# --------------------------------------------------

# X contains input features only.
# The five target scores are excluded to prevent data leakage.

X = df.drop(columns=targets)
y = df[targets]

# Remove columns that contain no useful values.
empty_columns = X.columns[X.isna().all()].tolist()

if empty_columns:
    X = X.drop(columns=empty_columns)
    print("\nEmpty input columns removed:", empty_columns)

if X.shape[1] == 0:
    raise ValueError("No usable input features were found.")

# Identify categorical and numerical input columns.
categorical_columns = X.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    include=["number"]
).columns.tolist()

unsupported_columns = [
    col for col in X.columns
    if col not in categorical_columns
    and col not in numerical_columns
]

if unsupported_columns:
    raise ValueError(
        f"Please check these unsupported input columns: "
        f"{unsupported_columns}"
    )

print("\nNumber of numerical features:", len(numerical_columns))
print("Number of categorical features:", len(categorical_columns))
print("Input features:", X.shape[1])


# --------------------------------------------------
# 4. PREPROCESS THE DATA
# --------------------------------------------------

# Numerical features:
# Fill missing values using the median.

numerical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

# Categorical features:
# Fill missing values using the most frequent value.
# Convert categories into numerical columns using One-Hot Encoding.

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# Combine both preprocessing pipelines.

preprocessor = ColumnTransformer(transformers=[
    ("numerical", numerical_pipeline, numerical_columns),
    ("categorical", categorical_pipeline, categorical_columns)
])


# --------------------------------------------------
# 5. SPLIT DATA INTO TRAINING AND TESTING SETS
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# --------------------------------------------------
# 6. CREATE AND TRAIN THE MODEL
# --------------------------------------------------

# Linear Regression predicts all five target scores.

model = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("regression", LinearRegression())
])

print("\nTraining Linear Regression model...")

model.fit(X_train, y_train)

print("Model training completed successfully!")


# --------------------------------------------------
# 7. PREDICT THE FIVE RISK SCORES
# --------------------------------------------------

y_pred = model.predict(X_test)

# Keep the original predictions for evaluation.
# Predictions are not clipped to a range because clipping
# would change the model's raw outputs.


# --------------------------------------------------
# 8. EVALUATE MODEL PERFORMANCE
# --------------------------------------------------

results = []

print("\n" + "=" * 85)
print("                    MODEL EVALUATION")
print("=" * 85)

print(
    f"{'Target':<30}"
    f"{'MAE':>10}"
    f"{'MSE':>12}"
    f"{'RMSE':>12}"
    f"{'RSS':>15}"
    f"{'R2':>10}"
)

print("-" * 89)

for index, target in enumerate(targets):

    actual = y_test[target].to_numpy()
    predicted = y_pred[:, index]

    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = mse ** 0.5

    residuals = actual - predicted
    rss = (residuals ** 2).sum()

    r2 = r2_score(actual, predicted)

    results.append({
        "Target": target,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "RSS": rss,
        "R2": r2
    })

    print(
        f"{target:<30}"
        f"{mae:>10.3f}"
        f"{mse:>12.3f}"
        f"{rmse:>12.3f}"
        f"{rss:>15.3f}"
        f"{r2:>10.3f}"
    )

print("-" * 89)

# Calculate average performance across the five targets.
results_df = pd.DataFrame(results)

print("\nAverage MAE:", round(results_df["MAE"].mean(), 3))
print("Average MSE:", round(results_df["MSE"].mean(), 3))
print("Average RMSE:", round(results_df["RMSE"].mean(), 3))
print("Average R2:", round(results_df["R2"].mean(), 3))


# --------------------------------------------------
# 9. SAVE EVALUATION RESULTS
# --------------------------------------------------

results_df.to_csv("model_evaluation.csv", index=False)

print("\nEvaluation results saved to model_evaluation.csv")


# --------------------------------------------------
# 10. SAVE ACTUAL AND PREDICTED TEST VALUES
# --------------------------------------------------

predictions_df = pd.DataFrame(index=y_test.index)

for index, target in enumerate(targets):
    predictions_df["Actual_" + target] = y_test[target].to_numpy()
    predictions_df["Predicted_" + target] = y_pred[:, index]

predictions_df.to_csv("test_predictions.csv", index=False)

print("Test predictions saved to test_predictions.csv")


# --------------------------------------------------
# 11. SAVE THE TRAINED MODEL
# --------------------------------------------------

joblib.dump(model, "healthscore_model.joblib")

print("Trained model saved to healthscore_model.joblib")

# --------------------------------------------------
# 12. CALCULATE OVERALL MODEL PERFORMANCE
# --------------------------------------------------

import numpy as np

# Load existing test predictions without retraining the model.
predictions = pd.read_csv("test_predictions.csv")

# Collect actual and predicted values for all five targets.
actual_columns = [
    "Actual_diabetes_risk_score",
    "Actual_hypertension_risk_score",
    "Actual_heart_disease_risk_score",
    "Actual_obesity_risk_score",
    "Actual_cholesterol_risk_score"
]

predicted_columns = [
    "Predicted_diabetes_risk_score",
    "Predicted_hypertension_risk_score",
    "Predicted_heart_disease_risk_score",
    "Predicted_obesity_risk_score",
    "Predicted_cholesterol_risk_score"
]

actual = predictions[actual_columns].to_numpy().ravel()
predicted = predictions[predicted_columns].to_numpy().ravel()

# Calculate overall regression metrics.
overall_mae = mean_absolute_error(actual, predicted)
overall_mse = mean_squared_error(actual, predicted)
overall_rmse = np.sqrt(overall_mse)
overall_rss = np.sum((actual - predicted) ** 2)

# Average the five individual R2 scores from model_evaluation.csv.
evaluation = pd.read_csv("model_evaluation.csv")
overall_r2 = evaluation["R2"].mean()

# Save the overall results in a separate file.
overall_results = pd.DataFrame([{
    "Overall_MAE": overall_mae,
    "Overall_MSE": overall_mse,
    "Overall_RMSE": overall_rmse,
    "Overall_RSS": overall_rss,
    "Mean_R2": overall_r2,
    "Mean_R2_Percentage_Equivalent": overall_r2 * 100
}])

overall_results.to_csv(
    "overall_model_evaluation.csv",
    index=False
)

print("\n" + "=" * 55)
print("       OVERALL MODEL PERFORMANCE")
print("=" * 55)
print(f"Overall MAE: {overall_mae:.3f}")
print(f"Overall MSE: {overall_mse:.3f}")
print(f"Overall RMSE: {overall_rmse:.3f}")
print(f"Overall RSS: {overall_rss:.3f}")
print(f"Mean R2 across five targets: {overall_r2:.4f}")
print(
    "Mean R2 percentage equivalent: "
    f"{overall_r2 * 100:.2f}%"
)
print("\nSaved to overall_model_evaluation.csv")
print("=" * 55)

# --------------------------------------------------
# 13. FINISH
# --------------------------------------------------

print("\n" + "=" * 60)
print("       MACHINE LEARNING PIPELINE COMPLETED")
print("=" * 60)

print("\nFiles created:")
print("1. healthscore_model.joblib")
print("2. model_evaluation.csv")
print("3. test_predictions.csv")

print("\nNext step: Review the model's performance before")
print("connecting it to the HealthScore AI application.")
