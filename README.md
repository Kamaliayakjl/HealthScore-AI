🩺 HealthScore AI

AI-Based Health Risk Assessment System

An academic machine-learning project that analyzes health and lifestyle data to estimate health-related risk scores through an interactive web application.

------------------------
🤝 TEAM MEMBERS (2)

This project was developed collaboratively as part of an academic contribution project.

👩‍💻 Contributor 1: [Kajal k. Kamaliya](⭐Project Lead)

👩‍💻 Contributor 2: [Ankita Rajput]


🌟 About the Project

HealthScore AI demonstrates how supervised machine learning can be used to analyze health-related data and estimate five health risk scores.

The project combines data preparation, exploratory data analysis, model training, model evaluation, and an interactive Streamlit application.

🎯 Project Objectives

- 📂 Prepare and analyze health-related data.
- 🧹 Validate and process the dataset.
- 🤖 Train a supervised machine-learning model.
- 🩺 Estimate five health-related risk scores.
- 📊 Evaluate model performance using regression metrics.
- 🌐 Display results through an interactive web application.
- 💡 Provide educational diet and lifestyle recommendations.

✨ Key Features

- 📝 Interactive health assessment form
- 🤖 Machine-learning-based risk-score estimation
- 📊 Univariate data analysis
- 📈 Bivariate data analysis
- 🔍 Multivariate data analysis
- 📉 Model evaluation and visualizations
- 🩺 Overall Health Score calculation
- 💡 Educational diet and lifestyle recommendations

⚙️ How It Works

1. 📂 Load the health dataset.
2. 🧹 Prepare and validate the data.
3. ✂️ Select 1,500 records for the project.
4. 🤖 Train the Linear Regression model.
5. 📊 Evaluate model performance.
6. 💾 Save the trained model.
7. 🌐 Run the Streamlit application.
8. 🩺 Display estimated scores and visualizations.


📚 Dataset Source

The dataset used in this project was obtained from Kaggle.

🔗 Original Dataset: [https://www.kaggle.com/datasets/tanyamishra260/health-risk-predictor-dataset]

📌 Only 1,500 records from the original dataset have been used in this project.


🧠 Machine Learning Model

The project uses Linear Regression, a supervised machine-learning algorithm, to estimate five target scores:

- Diabetes risk score
- Hypertension risk score
- Heart disease risk score
- Obesity risk score
- Cholesterol risk score

The model learns patterns between the input features and target scores in the selected dataset.
These scores are estimates based on the dataset and are not guaranteed predictions of future diseases.

🩺 Overall Health Score

The application calculates an overall score separately from the five predicted risk scores.

Formula:

Overall Health Score = 100 − Average of the Five Predicted Risk Scores

This calculation is performed only when all five predicted scores fall within the expected range of 0–100.
The overall score is a project-defined summary, not a clinically validated health measurement.

🛠️ Technologies Used

- 🐍 Python
- 🐼 Pandas
- 🤖 Scikit-learn
- 🌐 Streamlit
- 📊 Plotly
- 💾 Joblib

📁 Project Structure

- "app.py" — Runs the Streamlit web application.
- "prepare_data.py" — Prepares and processes the dataset.
- "prepare_model.py" — Trains and evaluates the machine-learning model.
- "validate_sample.py" — Performs dataset validation checks.
- "diet_plan.py" — Contains diet-plan functionality.
- "recommendations.py" — Contains recommendation functionality.
- "healthscore_1500.csv" — Dataset sample containing 1,500 records.
- "healthscore_model.joblib" — Saved trained model.
- "model_evaluation.csv" — Model evaluation results.
- "overall_model_evaluation.csv" — Overall evaluation results.
- "requirements.txt" — Python package dependencies.
- ".gitignore" — Specifies files Git should ignore.

🚀 Installation and Setup

1. Clone the Repository

git clone <my-repository-url>

2. Open the Project Folder

cd Healthcare_AI

3. Install Dependencies

pip install -r requirements.txt

4. Run the Application

streamlit run app.py

Open the local address displayed in the terminal to access the application.

📊 Model Evaluation

The project uses regression metrics to evaluate prediction errors and model performance.

- MAE: Mean Absolute Error
- MSE: Mean Squared Error
- RMSE: Root Mean Squared Error
- RSS: Residual Sum of Squares
- R²: Coefficient of Determination

These metrics help assess how closely the predicted scores match the target values.
A high R² score alone does not establish medical validity or guarantee accurate predictions for real people.




💻 GitHub Contribution Workflow

The project uses Git and GitHub to demonstrate collaborative development and version control.

- 📦 Creating and maintaining a GitHub repository
- 📝 Maintaining project documentation
- 💾 Making meaningful commits
- 🌿 Creating and working with branches
- 🔀 Opening a pull request
- ✅ Reviewing and merging a pull request
- 🏷️ Creating a version tag ("v1.0")

The repository's commit history, pull request, and version tag provide evidence of the contribution workflow.


⚠️ Limitations

- The project uses an existing dataset.
- The model learns patterns present in the selected data.
- Dataset quality and the original method used to create the target scores may affect performance.
- Predicted scores are estimates, not confirmed medical outcomes.
- The overall Health Score is not a validated clinical measurement.

This project is intended for educational purposes only. It must not be used for medical diagnosis or treatment decisions.


🔮 Future Improvements

- 🚀 Compare additional machine-learning algorithms.
- 🧹 Improve data validation and error handling.
- 📊 Add more informative visualizations.
- 🧪 Strengthen model testing and evaluation.
- 💡 Improve explanations of model predictions.
- 🌐 Enhance the application's usability.
- 📚 Improve dataset documentation.

---

🎓 Project Purpose

HealthScore AI demonstrates data preparation, exploratory data analysis, supervised machine learning, model evaluation, and interactive application development while providing practical experience with Git, GitHub, commits, branches, pull requests, and version tagging.

⚠️ Disclaimer: HealthScore AI is an academic project, not a medical device. Its predictions and recommendations are not a substitute for professional medical advice.