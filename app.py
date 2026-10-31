import os
import html

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from recommendations import generate_recommendations
from diet_plan import generate_diet_plan


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="HealthScore AI",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "healthscore_1500.csv")
MODEL_FILE = os.path.join(BASE_DIR, "healthscore_model.joblib")
EVALUATION_FILE = os.path.join(BASE_DIR, "model_evaluation.csv")
PREDICTIONS_FILE = os.path.join(BASE_DIR, "test_predictions.csv")

TARGETS = [
    "diabetes_risk_score",
    "hypertension_risk_score",
    "heart_disease_risk_score",
    "obesity_risk_score",
    "cholesterol_risk_score",
]

SCORE_LABELS = {
    "diabetes_risk_score": "Diabetes",
    "hypertension_risk_score": "Hypertension",
    "heart_disease_risk_score": "Heart Disease",
    "obesity_risk_score": "Obesity",
    "cholesterol_risk_score": "Cholesterol",
}

DISPLAY_ORDER = [
    "Diabetes",
    "Hypertension",
    "Heart Disease",
    "Obesity",
    "Cholesterol",
]

DIET_OPTIONS = [
    "Vegetarian",
    "Non-Vegetarian",
    "Vegan",
]

BUDGET_OPTIONS = ["Low", "Moderate", "High"]

COOKING_OPTIONS = [
    "Quick (15 minutes or less)",
    "Moderate",
    "Flexible",
]


# =========================================================
# 2. LOAD PROJECT FILES
# =========================================================

@st.cache_data
def load_dataset(path):
    return pd.read_csv(path)


@st.cache_resource
def load_model(path):
    return joblib.load(path)


if not os.path.exists(DATA_FILE):
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()

if not os.path.exists(MODEL_FILE):
    st.error(f"Trained model not found: {MODEL_FILE}")
    st.stop()

try:
    df = load_dataset(DATA_FILE)
    model = load_model(MODEL_FILE)

except Exception as exc:
    st.error(f"Could not load project files: {exc}")
    st.stop()


missing_targets = [
    target for target in TARGETS
    if target not in df.columns
]

if missing_targets:
    st.error(
        "The dataset is missing expected target columns: "
        + ", ".join(missing_targets)
    )
    st.stop()


# =========================================================
# 3. DETERMINE MODEL INPUT FEATURES
# =========================================================

def find_feature_columns():
    candidates = getattr(model, "feature_names_in_", None)

    if candidates is None and hasattr(model, "named_steps"):
        final_estimator = model.named_steps.get("model")

        if final_estimator is not None:
            candidates = getattr(
                final_estimator,
                "feature_names_in_",
                None,
            )

    if candidates is None:
        candidates = [
            column for column in df.columns
            if column not in TARGETS
        ]

    columns = [
        column for column in candidates
        if column in df.columns and column not in TARGETS
    ]

    return columns


FEATURE_COLUMNS = find_feature_columns()

if not FEATURE_COLUMNS:
    st.error(
        "Could not determine the model input features. "
        "Check how healthscore_model.joblib was trained."
    )
    st.stop()


# =========================================================
# 4. SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "assessment_complete": False,
    "prediction_results": None,
    "prediction_inputs": {},
    "health_score": None,
    "dietary_preferences": {},
    "navigation_page": "Home Dashboard",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 5. NAVIGATION CALLBACK
# =========================================================

def go_to_assessment():
    st.session_state["navigation_page"] = "Health Assessment"


# =========================================================
# 6. DARK THEME
# =========================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --bg: #08111f;
        --panel: #111e30;
        --border: #2b3c52;
        --text: #f2f6fc;
        --muted: #b4c2d5;
        --teal: #38e0c0;
        --blue: #62b4ff;
        --coral: #ff8b83;
        --purple: #bba3ff;
    }

    html, body, [class*="css"] {
        font-family: Inter, sans-serif;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(8,17,31,.95);
    }

    [data-testid="stSidebar"] {
        background: #0d192a;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    h1, h2, h3, h4, p, label, li {
        color: var(--text);
    }

    p, label, li {
        line-height: 1.65;
    }

    .hero {
        padding: 30px;
        border-radius: 22px;
        background:
          radial-gradient(circle at 85% 15%,
          rgba(56,224,192,.19), transparent 35%),
          linear-gradient(135deg, #14283d, #111b2c);
        border: 1px solid #30445d;
        margin-bottom: 24px;
    }

    .hero-tag {
        color: var(--teal);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 12px;
        font-weight: 800;
    }

    .hero h1 {
        font-size: clamp(30px, 4vw, 46px);
        margin: 12px 0;
        font-weight: 800;
        color: #fff;
    }

    .hero p {
        color: #d0dbea;
        font-size: 15px;
        max-width: 760px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 800;
        margin-top: 22px;
        margin-bottom: 6px;
        color: #fff;
    }

    .metric-card {
        background: linear-gradient(145deg, #16263b, #101b2b);
        border: 1px solid #33465d;
        padding: 21px;
        border-radius: 18px;
        min-height: 145px;
        margin-bottom: 12px;
    }

    .metric-label {
        color: #c8d5e5;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 800;
        color: #fff;
        margin-top: 8px;
    }

    .metric-caption {
        color: #b8c7d8;
        font-size: 12px;
        margin-top: 7px;
    }

    .accent-line {
        height: 4px;
        width: 55px;
        border-radius: 10px;
        background: var(--teal);
        margin-top: 14px;
    }

    .info-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .info-card h3 {
        font-size: 17px;
        margin-top: 0;
        color: #fff;
    }

    .info-card p {
        color: #cfdae8;
        font-size: 14px;
    }

    .tag {
        display: inline-block;
        background: #183e43;
        color: #8ff7e2;
        padding: 5px 10px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: #36d9b8;
        color: #07151e;
        border: none;
        border-radius: 10px;
        font-weight: 800;
        min-height: 44px;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #83f4df;
        color: #07151e;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background: #132238;
        color: white;
        border: 1px solid #3b5069;
        border-radius: 9px;
    }

    [data-baseweb="select"] > div {
        background: #132238;
        color: white;
        border-color: #3b5069;
    }

    [data-testid="stMetric"] {
        background: #14243a;
        border: 1px solid #344960;
        padding: 15px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #c7d6e7;
    }

    [data-testid="stMetricValue"] {
        color: white;
    }

    hr {
        border-color: #2c3e54;
    }

    .small-note {
        font-size: 12px;
        color: #bac8d9;
    }

    .stCaption {
        color: #c0cede;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 7. HELPER FUNCTIONS
# =========================================================

def safe_float(value, default=0.0):
    try:
        value = float(value)
        return value if np.isfinite(value) else default
    except (TypeError, ValueError):
        return default


def score_color(score):
    if score < 30:
        return "#38e0c0"
    if score < 60:
        return "#ffbd66"
    return "#ff8b83"


def render_hero(title, subtitle, tag="HEALTHSCORE AI"):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-tag">{html.escape(tag)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value, caption="", color=None):
    color = color or "#38e0c0"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value" style="color:{color}">
                {html.escape(str(value))}
            </div>
            <div class="metric-caption">{html.escape(str(caption))}</div>
            <div class="accent-line" style="background:{color}"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(title, description, icon="✦"):
    st.markdown(
        f"""
        <div class="info-card">
            <h3>{icon} &nbsp; {html.escape(str(title))}</h3>
            <p>{html.escape(str(description))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_score_cards(scores):
    columns = st.columns(2)

    for index, name in enumerate(DISPLAY_ORDER):
        score = safe_float(scores.get(name, 0))
        color = score_color(score)

        with columns[index % 2]:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{html.escape(name)}</div>
                    <div class="metric-value" style="color:{color}">
                        {score:.1f}
                        <span style="font-size:14px;color:#c0cede">
                            / 100
                        </span>
                    </div>
                    <div style="background:#2b3c52;height:8px;
                                border-radius:8px;margin-top:12px">
                        <div style="background:{color};
                                    width:{max(0,min(100,score))}%;
                                    height:8px;border-radius:8px">
                        </div>
                    </div>
                    <div class="metric-caption">
                        Project-generated score; not a diagnosis
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def make_plotly_dark(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#edf4ff", family="Inter"),
        height=height,
        margin=dict(l=25, r=25, t=45, b=25),
    )
    return fig


def get_default_value(column):
    series = df[column]

    if pd.api.types.is_numeric_dtype(series):
        numeric = pd.to_numeric(series, errors="coerce").dropna()

        if numeric.empty:
            return 0.0

        return float(numeric.median())

    values = series.dropna().astype(str).unique().tolist()

    return str(values[0]) if values else ""


def get_input_widget(column, section_key):
    """Create a widget appropriate to the dataset column."""

    series = df[column]
    widget_key = f"{section_key}_{column}"

    if pd.api.types.is_numeric_dtype(series):
        values = pd.to_numeric(series, errors="coerce").dropna()

        if values.empty:
            return st.number_input(
                column,
                value=0.0,
                key=widget_key,
            )

        minimum = float(values.min())
        maximum = float(values.max())
        default = float(values.median())

        if minimum == maximum:
            return st.number_input(
                column,
                value=default,
                key=widget_key,
            )

        return st.number_input(
            column,
            min_value=minimum,
            max_value=maximum,
            value=min(max(default, minimum), maximum),
            key=widget_key,
        )

    options = sorted(
        series.dropna().astype(str).unique().tolist()
    )

    if not options:
        return ""

    return st.selectbox(
        column,
        options,
        key=widget_key,
    )


# =========================================================
# 8. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding:18px 4px 24px">
            <div style="font-size:12px;color:#38e0c0;
                        font-weight:800;letter-spacing:2px">
                HEALTH TECH
            </div>
            <div style="font-size:29px;font-weight:800;
                        color:white;margin-top:5px">
                HealthScore <span style="color:#38e0c0">AI</span>
            </div>
            <div style="color:#b7c7d9;font-size:12px">
                Your educational health analytics dashboard
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Home Dashboard",
            "Health Assessment",
            "Personalized Recommendations",
            "Personalized Diet Plan",
            "Univariate Analysis",
            "Bivariate Analysis",
            "Multivariate Analysis",
            "Model Evaluation",
        ],
        key="navigation_page",
    )

    st.divider()

    st.markdown(
        """
        <div class="small-note">
            COLLEGE ML PROJECT<br><br>
            Outputs are educational demonstrations, not medical
            diagnoses or validated clinical risk estimates.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 9. HOME DASHBOARD
# =========================================================

if page == "Home Dashboard":

    render_hero(
        "Understand your health data.",
        "Explore model-generated scores, lifestyle insights, "
        "personalized educational recommendations and meal ideas.",
    )

    st.markdown(
        '<div class="section-title">Project overview</div>',
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)

    with a:
        render_metric_card(
            "Dataset records",
            f"{len(df):,}",
            "Rows available to this project",
            "#62b4ff",
        )

    with b:
        render_metric_card(
            "Input features",
            len(FEATURE_COLUMNS),
            "Features used by the model",
            "#38e0c0",
        )

    with c:
        render_metric_card(
            "Model outputs",
            len(TARGETS),
            "Separate score predictions",
            "#bba3ff",
        )

    with d:
        render_metric_card(
            "Assessment",
            "Complete" if st.session_state.assessment_complete
            else "Not started",
            "Latest assessment status",
            "#ffbd66",
        )

    if st.session_state.assessment_complete:
        st.markdown(
            '<div class="section-title">Your latest assessment</div>',
            unsafe_allow_html=True,
        )

        left, right = st.columns([1, 2])

        with left:
            render_metric_card(
                "Project-defined Health Score",
                f"{st.session_state.health_score:.1f}/100",
                "100 minus the average of five displayed scores",
                "#38e0c0",
            )

        with right:
            render_score_cards(
                st.session_state.prediction_results
            )

        st.info(
            "This is a project-defined summary, not a medically "
            "validated health measurement."
        )

        chart_data = pd.DataFrame({
            "Category": DISPLAY_ORDER,
            "Score": [
                st.session_state.prediction_results[name]
                for name in DISPLAY_ORDER
            ],
        })

        fig = px.bar(
            chart_data,
            x="Category",
            y="Score",
            color="Category",
            title="Your five model-generated scores",
            range_y=[0, 100],
        )

        st.plotly_chart(
            make_plotly_dark(fig),
            use_container_width=True,
        )

    else:
        render_info_card(
            "Start with an assessment",
            "Enter the available demographic, lifestyle and "
            "health-related inputs to generate five model outputs.",
            "01",
        )

        st.button(
            "Go to Health Assessment",
            use_container_width=True,
            on_click=go_to_assessment,
        )

    st.markdown(
        '<div class="section-title">Explore your application</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        render_info_card(
            "Lifestyle Recommendations",
            "Review educational suggestions based on your saved inputs "
            "and model-generated outputs.",
            "✦",
        )

    with c2:
        render_info_card(
            "Personalized Meal Suggestions",
            "Explore meal ideas based on your dietary preference, "
            "allergies, budget and cooking time.",
            "◈",
        )

    with c3:
        render_info_card(
            "Data Analysis",
            "Explore distributions, relationships and correlations "
            "in the dataset.",
            "▦",
        )


# =========================================================
# 10. HEALTH ASSESSMENT
# =========================================================

elif page == "Health Assessment":

    render_hero(
        "Health Assessment",
        "Enter your information and submit the form to generate "
        "updated model predictions.",
        "PERSONALIZED INPUTS",
    )

    st.info(
        "Editing a field alone does not update the results. "
        "Select Generate My Assessment to run the model again."
    )

    input_values = {}

    demographic_columns = [
        col for col in FEATURE_COLUMNS
        if any(
            word in col.lower()
            for word in [
                "age", "gender", "ethnicity",
                "education", "income", "employment",
            ]
        )
    ]

    lifestyle_columns = [
        col for col in FEATURE_COLUMNS
        if col not in demographic_columns
        and any(
            word in col.lower()
            for word in [
                "smoking", "alcohol", "physical_activity",
                "diet_score", "sleep", "screen_time",
            ]
        )
    ]

    history_columns = [
        col for col in FEATURE_COLUMNS
        if col not in demographic_columns
        and col not in lifestyle_columns
        and any(
            word in col.lower()
            for word in ["history", "family"]
        )
    ]

    measurement_columns = [
        col for col in FEATURE_COLUMNS
        if col not in demographic_columns
        and col not in lifestyle_columns
        and col not in history_columns
    ]

    with st.form("health_assessment_form"):

        st.markdown("### 01 · Demographic information")
        columns = st.columns(2)

        for index, column in enumerate(demographic_columns):
            with columns[index % 2]:
                input_values[column] = get_input_widget(
                    column, "assessment"
                )

        st.markdown("### 02 · Lifestyle information")
        columns = st.columns(2)

        for index, column in enumerate(lifestyle_columns):
            with columns[index % 2]:
                input_values[column] = get_input_widget(
                    column, "assessment"
                )

        st.markdown("### 03 · Health history")
        columns = st.columns(2)

        for index, column in enumerate(history_columns):
            with columns[index % 2]:
                input_values[column] = get_input_widget(
                    column, "assessment"
                )

        st.markdown("### 04 · Health measurements")
        columns = st.columns(2)

        for index, column in enumerate(measurement_columns):
            with columns[index % 2]:
                input_values[column] = get_input_widget(
                    column, "assessment"
                )

        st.divider()
        st.markdown("### 05 · Dietary preferences")

        left, right = st.columns(2)

        with left:
            dietary_preference = st.selectbox(
                "Dietary preference",
                DIET_OPTIONS,
                key="assessment_dietary_preference",
            )

            food_budget = st.selectbox(
                "Food budget",
                BUDGET_OPTIONS,
                key="assessment_food_budget",
            )

            cooking_time = st.selectbox(
                "Available cooking time",
                COOKING_OPTIONS,
                key="assessment_cooking_time",
            )

        with right:
            liked_foods = st.text_input(
                "Foods you like",
                placeholder="e.g. rice, paneer, eggs, chicken",
                key="assessment_liked_foods",
            )

            food_allergies = st.text_input(
                "Food allergies",
                placeholder="Comma-separated, e.g. peanuts, milk",
                key="assessment_food_allergies",
            )

            foods_to_avoid = st.text_input(
                "Foods to avoid",
                placeholder="e.g. mushrooms, fish",
                key="assessment_foods_to_avoid",
            )

        submitted = st.form_submit_button(
            "Generate My Assessment",
            use_container_width=True,
        )

    if submitted:
        try:
            model_input = pd.DataFrame(
                [input_values],
                columns=FEATURE_COLUMNS,
            )

            # The model must receive the same columns, in the same
            # order, that were used when training it.
            predictions = np.asarray(model.predict(model_input))

            if predictions.ndim == 1:
                predictions = predictions.reshape(1, -1)

            if predictions.shape != (1, len(TARGETS)):
                st.error(
                    "The model did not return exactly five predictions. "
                    "Check the model and target configuration."
                )
                st.stop()

            raw_scores = {
                SCORE_LABELS[target]: float(predictions[0][index])
                for index, target in enumerate(TARGETS)
            }

            if not all(
                np.isfinite(value)
                for value in raw_scores.values()
            ):
                st.error(
                    "The model returned an invalid numeric prediction. "
                    "Please check the model and inputs."
                )
                st.stop()

            outside_range = {
                name: value
                for name, value in raw_scores.items()
                if value < 0 or value > 100
            }

            # Clip only for display and the project-defined summary.
            # Preserve the fact that the raw model output was out of range.
            scores = {
                name: float(np.clip(value, 0, 100))
                for name, value in raw_scores.items()
            }

            dietary_preferences = {
                "dietary_preference": dietary_preference,
                "food_budget": food_budget,
                "cooking_time": cooking_time,
                "liked_foods": liked_foods,
                "food_allergies": food_allergies,
                "foods_to_avoid": foods_to_avoid,
            }

            combined_inputs = dict(input_values)
            combined_inputs.update(dietary_preferences)

            st.session_state.prediction_inputs = combined_inputs
            st.session_state.dietary_preferences = dietary_preferences
            st.session_state.prediction_results = scores
            st.session_state.raw_prediction_results = raw_scores

            st.session_state.health_score = float(
                100 - np.mean(list(scores.values()))
            )

            st.session_state.assessment_complete = True

            if outside_range:
                st.session_state.prediction_range_warning = True
            else:
                st.session_state.prediction_range_warning = False

            st.success(
                "New assessment generated from your submitted inputs."
            )

            st.rerun()

        except Exception as exc:
            st.error(f"Assessment failed: {exc}")

    if st.session_state.assessment_complete:
        st.markdown("### Your latest results")

        if st.session_state.get("prediction_range_warning", False):
            st.warning(
                "One or more raw model predictions fell outside 0–100. "
                "The displayed values were clipped to that range. "
                "This should be investigated when evaluating the model."
            )

        render_score_cards(
            st.session_state.prediction_results
        )

        st.caption(
            "These results reflect the last successfully submitted "
            "assessment. Submit the form again after changing inputs."
        )


# =========================================================
# 11. PERSONALIZED RECOMMENDATIONS
# =========================================================

elif page == "Personalized Recommendations":

    render_hero(
        "Your Recommendations",
        "Educational suggestions based on your saved assessment "
        "inputs and model-generated scores.",
        "PERSONALIZED INSIGHTS",
    )

    if not st.session_state.assessment_complete:
        st.warning(
            "Complete Health Assessment first to generate "
            "personalized recommendations."
        )

    else:
        try:
            recommendations = generate_recommendations(
                st.session_state.prediction_inputs,
                st.session_state.prediction_results,
            )

            section_icons = {
                "Diet Recommendations": "🥗",
                "Lifestyle Recommendations": "✦",
                "General Tips": "◈",
            }

            for section, icon in section_icons.items():
                st.markdown(
                    f'<div class="section-title">'
                    f'{icon} {html.escape(section)}</div>',
                    unsafe_allow_html=True,
                )

                items = recommendations.get(section, [])

                if not items:
                    st.info(
                        "No suggestions were returned for this section."
                    )
                    continue

                columns = st.columns(2)

                for index, item in enumerate(items):
                    if isinstance(item, dict):
                        title = str(
                            item.get("title", "Suggestion")
                        )
                        description = str(
                            item.get("description", "")
                        )
                    else:
                        title = "Suggestion"
                        description = str(item)

                    with columns[index % 2]:
                        render_info_card(
                            title, description, icon
                        )

        except Exception as exc:
            st.error(
                f"Could not generate recommendations: {exc}"
            )

        st.info(
            "These suggestions are educational, not medical advice. "
            "The model's scores are not diagnoses."
        )


# =========================================================
# 12. PERSONALIZED DIET PLAN
# =========================================================

elif page == "Personalized Diet Plan":

    render_hero(
        "Your Personalized Meal Plan",
        "Update your dietary preferences here without repeating "
        "the health assessment.",
        "PERSONALIZED NUTRITION IDEAS",
    )

    if not st.session_state.assessment_complete:
        st.warning(
            "Complete Health Assessment first. "
            "Your meal plan uses the saved assessment."
        )

    else:
        saved_preferences = dict(
            st.session_state.dietary_preferences
        )

        if not saved_preferences:
            saved_preferences = {
                key: st.session_state.prediction_inputs.get(key, default)
                for key, default in {
                    "dietary_preference": "Vegetarian",
                    "food_budget": "Moderate",
                    "cooking_time": "Moderate",
                    "liked_foods": "",
                    "food_allergies": "",
                    "foods_to_avoid": "",
                }.items()
            }

        st.markdown("### Update your meal preferences")

        with st.form("diet_preferences_update_form"):
            left, right = st.columns(2)

            with left:
                diet_value = saved_preferences.get(
                    "dietary_preference", "Vegetarian"
                )
                diet_index = (
                    DIET_OPTIONS.index(diet_value)
                    if diet_value in DIET_OPTIONS else 0
                )

                new_diet = st.selectbox(
                    "Dietary preference",
                    DIET_OPTIONS,
                    index=diet_index,
                    key="diet_page_preference",
                )

                budget_value = saved_preferences.get(
                    "food_budget", "Moderate"
                )
                budget_index = (
                    BUDGET_OPTIONS.index(budget_value)
                    if budget_value in BUDGET_OPTIONS else 1
                )

                new_budget = st.selectbox(
                    "Food budget",
                    BUDGET_OPTIONS,
                    index=budget_index,
                    key="diet_page_budget",
                )

                cooking_value = saved_preferences.get(
                    "cooking_time", "Moderate"
                )
                cooking_index = (
                    COOKING_OPTIONS.index(cooking_value)
                    if cooking_value in COOKING_OPTIONS else 1
                )

                new_cooking = st.selectbox(
                    "Available cooking time",
                    COOKING_OPTIONS,
                    index=cooking_index,
                    key="diet_page_cooking",
                )

            with right:
                new_liked = st.text_input(
                    "Foods you like",
                    value=str(saved_preferences.get("liked_foods", "")),
                    key="diet_page_liked",
                )

                new_allergies = st.text_input(
                    "Food allergies",
                    value=str(saved_preferences.get("food_allergies", "")),
                    key="diet_page_allergies",
                )

                new_avoid = st.text_input(
                    "Foods to avoid",
                    value=str(saved_preferences.get("foods_to_avoid", "")),
                    key="diet_page_avoid",
                )

            save_preferences = st.form_submit_button(
                "Save Preferences & Update Meal Plan",
                use_container_width=True,
            )

        if save_preferences:
            updated_preferences = {
                "dietary_preference": new_diet,
                "food_budget": new_budget,
                "cooking_time": new_cooking,
                "liked_foods": new_liked,
                "food_allergies": new_allergies,
                "foods_to_avoid": new_avoid,
            }

            st.session_state.dietary_preferences = (
                updated_preferences
            )

            st.session_state.prediction_inputs.update(
                updated_preferences
            )

            st.session_state["diet_preferences_updated"] = True

            st.rerun()

        user_input = dict(
            st.session_state.prediction_inputs
        )
        scores = st.session_state.prediction_results

        preference = user_input.get(
            "dietary_preference", "Vegetarian"
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="tag">CURRENT PREFERENCES</div>
                <h3>{html.escape(str(preference))}</h3>
                <p>
                    Budget: {html.escape(str(user_input.get('food_budget', 'Moderate')))}
                    <br>
                    Cooking time: {html.escape(str(user_input.get('cooking_time', 'Moderate')))}
                    <br>
                    Foods liked: {html.escape(str(user_input.get('liked_foods', '') or 'Not specified'))}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            plan_result = generate_diet_plan(
                user_input,
                scores,
            )

            meal_plan = plan_result.get("meal_plan", {})
            notes = plan_result.get("notes", [])
            preferences_used = plan_result.get(
                "preferences_used", {}
            )

            actual_preference = str(
                preferences_used.get(
                    "dietary_preference", ""
                )
            ).strip().lower().replace("_", "-")

            expected_preference = (
                str(preference).strip().lower().replace("_", "-")
            )

            aliases = {
                "non veg": "non-vegetarian",
                "non-veg": "non-vegetarian",
                "non vegetarian": "non-vegetarian",
                "non-vegetarian": "non-vegetarian",
                "veg": "vegetarian",
            }

            actual_preference = aliases.get(
                actual_preference, actual_preference
            )
            expected_preference = aliases.get(
                expected_preference, expected_preference
            )

            if (
                actual_preference
                and actual_preference != expected_preference
            ):
                st.warning(
                    "The meal generator's reported preference does not "
                    "match your saved preference. Check diet_plan.py."
                )

            st.markdown(
                '<div class="section-title">Your daily meal ideas</div>',
                unsafe_allow_html=True,
            )

            meal_icons = {
                "Breakfast": "☀️",
                "Lunch": "🥗",
                "Evening Snack": "🍎",
                "Dinner": "🌙",
            }

            meal_columns = st.columns(2)

            for index, (meal_type, options) in enumerate(
                meal_plan.items()
            ):
                with meal_columns[index % 2]:
                    st.markdown(
                        f"""
                        <div class="info-card">
                            <div class="tag">
                                {meal_icons.get(meal_type, '🍽️')}
                                &nbsp; MEAL
                            </div>
                            <h3>{html.escape(str(meal_type))}</h3>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    for meal in options:
                        st.markdown(
                            f"""
                            <div class="info-card"
                                 style="padding:13px 16px">
                                <p style="margin:0">
                                    {html.escape(str(meal))}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            st.markdown(
                '<div class="section-title">Personalized notes</div>',
                unsafe_allow_html=True,
            )

            for note in notes:
                st.markdown(
                    f"""
                    <div class="info-card">
                        <p>{html.escape(str(note))}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.expander(
                "View preferences received by the generator"
            ):
                st.json(preferences_used)

        except Exception as exc:
            st.error(f"Could not generate the meal plan: {exc}")

        st.info(
            "These meal ideas are educational, not a clinical diet "
            "prescription. Check ingredient labels and cross-contact "
            "risks for allergies. The generator only knows about "
            "ingredients represented in its meal database."
        )


# =========================================================
# 13. UNIVARIATE ANALYSIS
# =========================================================

elif page == "Univariate Analysis":

    render_hero(
        "Univariate Analysis",
        "Explore the distribution of one dataset variable at a time.",
        "DATA EXPLORATION",
    )

    selected_column = st.selectbox(
        "Choose a variable",
        df.columns.tolist(),
    )

    series = df[selected_column]

    a, b, c = st.columns(3)

    with a:
        render_metric_card(
            "Non-missing records",
            int(series.notna().sum()),
            selected_column,
            "#62b4ff",
        )

    with b:
        render_metric_card(
            "Unique values",
            int(series.nunique()),
            "Distinct observed values",
            "#38e0c0",
        )

    with c:
        render_metric_card(
            "Missing values",
            int(series.isna().sum()),
            "Values not recorded",
            "#ffbd66",
        )

    if pd.api.types.is_numeric_dtype(series):
        fig = px.histogram(
            df,
            x=selected_column,
            nbins=30,
            title=f"Distribution of {selected_column}",
        )

        st.plotly_chart(
            make_plotly_dark(fig),
            use_container_width=True,
        )

        st.dataframe(
            series.describe().to_frame("Statistics"),
            use_container_width=True,
        )

    else:
        counts = (
            series.astype(str)
            .value_counts()
            .head(20)
            .rename_axis("Category")
            .reset_index(name="Count")
        )

        fig = px.bar(
            counts,
            x="Category",
            y="Count",
            title=f"Category distribution: {selected_column}",
        )

        st.plotly_chart(
            make_plotly_dark(fig),
            use_container_width=True,
        )


# =========================================================
# 14. BIVARIATE ANALYSIS
# =========================================================

elif page == "Bivariate Analysis":

    render_hero(
        "Bivariate Analysis",
        "Explore the relationship between two dataset variables.",
        "RELATIONSHIP EXPLORATION",
    )

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if len(numeric_columns) < 2:
        st.warning("At least two numeric columns are required.")

    else:
        left, right = st.columns(2)

        with left:
            x_column = st.selectbox(
                "X-axis variable",
                numeric_columns,
                index=0,
            )

        with right:
            y_column = st.selectbox(
                "Y-axis variable",
                numeric_columns,
                index=min(1, len(numeric_columns) - 1),
            )

        plot_df = df[[x_column, y_column]].dropna()

        fig = px.scatter(
            plot_df,
            x=x_column,
            y=y_column,
            title=f"{x_column} vs {y_column}",
            opacity=0.7,
        )

        st.plotly_chart(
            make_plotly_dark(fig),
            use_container_width=True,
        )

        if len(plot_df) >= 2:
            correlation = plot_df[x_column].corr(
                plot_df[y_column]
            )

            render_metric_card(
                "Pearson correlation",
                f"{correlation:.3f}",
                "Correlation describes association, not causation.",
                "#62b4ff",
            )


# =========================================================
# 15. MULTIVARIATE ANALYSIS
# =========================================================

elif page == "Multivariate Analysis":

    render_hero(
        "Multivariate Analysis",
        "Examine relationships across several numeric variables.",
        "MULTIVARIATE EXPLORATION",
    )

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        st.warning(
            "Not enough numeric columns for this analysis."
        )

    else:
        selected_columns = st.multiselect(
            "Choose variables for the correlation heatmap",
            numeric_df.columns.tolist(),
            default=numeric_df.columns.tolist()[
                :min(10, len(numeric_df.columns))
            ],
        )

        if len(selected_columns) >= 2:
            correlation_matrix = numeric_df[
                selected_columns
            ].corr()

            fig = px.imshow(
                correlation_matrix,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Correlation heatmap",
            )

            st.plotly_chart(
                make_plotly_dark(fig, height=550),
                use_container_width=True,
            )

        else:
            st.info("Choose at least two variables.")


# =========================================================
# 16. MODEL EVALUATION
# =========================================================

elif page == "Model Evaluation":

    render_hero(
        "Model Evaluation",
        "Review saved evaluation metrics and test predictions "
        "from the trained project model.",
        "MODEL PERFORMANCE",
    )

    if os.path.exists(EVALUATION_FILE):
        evaluation_df = pd.read_csv(EVALUATION_FILE)

        st.markdown("### Saved evaluation metrics")

        st.dataframe(
            evaluation_df,
            use_container_width=True,
            hide_index=True,
        )

        numeric_metrics = evaluation_df.select_dtypes(
            include=np.number
        )

        if not numeric_metrics.empty:
            st.markdown("### Numeric metric overview")

            st.dataframe(
                numeric_metrics.describe().T,
                use_container_width=True,
            )

    else:
        st.warning(
            "model_evaluation.csv was not found. "
            "Saved evaluation metrics cannot be displayed."
        )

    if os.path.exists(PREDICTIONS_FILE):
        predictions_df = pd.read_csv(PREDICTIONS_FILE)

        st.markdown("### Test prediction data")

        st.dataframe(
            predictions_df.head(100),
            use_container_width=True,
        )

        st.caption(
            f"Showing up to 100 rows from "
            f"{len(predictions_df):,} saved prediction records."
        )

    else:
        st.warning("test_predictions.csv was not found.")

    st.markdown("### Metric definitions")

    left, right = st.columns(2)

    with left:
        render_info_card(
            "MAE",
            "Mean Absolute Error: average absolute difference "
            "between actual and predicted values.",
            "01",
        )

        render_info_card(
            "MSE",
            "Mean Squared Error: average squared prediction error.",
            "02",
        )

    with right:
        render_info_card(
            "RSS",
            "Residual Sum of Squares: the sum of squared errors.",
            "03",
        )

        render_info_card(
            "R²",
            "R-squared: a measure of how well the model explains "
            "variation in the evaluated target data.",
            "04",
        )

    st.info(
        "Evaluation metrics describe performance on the evaluated "
        "data. They do not establish clinical validity or guarantee "
        "real-world health prediction accuracy."
    )


# =========================================================
# 17. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:15px 0 25px;
                color:#b8c8da;font-size:12px">
        <b style="color:#38e0c0">HealthScore AI</b>
        &nbsp; · &nbsp; Student Machine Learning Project
        <br><br>
        Educational model outputs only. Not a medical diagnosis,
        validated clinical risk assessment or substitute for
        professional healthcare advice.
    </div>
    """,
    unsafe_allow_html=True,
)