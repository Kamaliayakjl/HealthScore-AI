def generate_recommendations(user_input, risk_scores):
    """
    Generate personalized educational recommendations.

    Parameters:
        user_input: Dictionary of health assessment inputs.
        risk_scores: Dictionary of five predicted risk scores.

    Returns:
        Dictionary containing diet, lifestyle, and general tips.
    """

    import math

    diet = []
    lifestyle = []
    general_tips = []

    # --------------------------------------------------
    # 1. HELPER FUNCTIONS
    # --------------------------------------------------

    def get_number(feature):
        """Safely retrieve a numeric user input."""
        value = user_input.get(feature)

        try:
            if value is None:
                return None

            number = float(value)

            if not math.isfinite(number):
                return None

            return number

        except (TypeError, ValueError):
            return None

    def get_score(category):
        """Safely retrieve a predicted score."""
        try:
            score = float(risk_scores.get(category))

            if not math.isfinite(score):
                return None

            return score

        except (TypeError, ValueError):
            return None

    # --------------------------------------------------
    # 2. GENERAL DIET RECOMMENDATIONS
    # --------------------------------------------------

    diet.append({
        "title": "Build balanced meals",
        "description": (
            "Include vegetables, fruits, whole grains, and "
            "fibre-rich foods in your regular meals."
        )
    })

    diet.append({
        "title": "Include protein sources",
        "description": (
            "Choose suitable protein sources such as dal, "
            "lentils, beans, chickpeas, tofu, curd, paneer, "
            "nuts, and seeds."
        )
    })

    diet.append({
        "title": "Choose healthier fats",
        "description": (
            "Include appropriate amounts of nuts, seeds, "
            "and unsaturated plant oils. Limit frequent "
            "intake of foods high in saturated or trans fats."
        )
    })

    diet.append({
        "title": "Choose drinks mindfully",
        "description": (
            "Prefer water or unsweetened drinks more often "
            "instead of frequently consuming sugary beverages."
        )
    })

    # --------------------------------------------------
    # 3. SCORE-RELATED EDUCATIONAL GUIDANCE
    # --------------------------------------------------
    # The threshold of 60 is for project demonstration only.
    # It is not a medically validated risk threshold.

    diabetes_score = get_score("Diabetes")

    if diabetes_score is not None and diabetes_score >= 60:
        diet.append({
            "title": "Blood glucose awareness",
            "description": (
                "Your model-generated diabetes-related score "
                "is relatively high under this project's "
                "demonstration rule. Consider balanced meals "
                "with fibre-rich foods and discuss appropriate "
                "screening with a healthcare professional."
            )
        })

    cholesterol_score = get_score("Cholesterol")

    if cholesterol_score is not None and cholesterol_score >= 60:
        diet.append({
            "title": "Heart-friendly food choices",
            "description": (
                "Consider foods rich in soluble fibre, such as "
                "oats, beans, and lentils. Limit frequent intake "
                "of foods high in saturated fats. A healthcare "
                "professional can interpret actual cholesterol tests."
            )
        })

    hypertension_score = get_score("Hypertension")

    if hypertension_score is not None and hypertension_score >= 60:
        diet.append({
            "title": "Be mindful of excess sodium",
            "description": (
                "Avoid excessive salt intake and check the sodium "
                "content of packaged foods. A model-generated score "
                "cannot establish whether you have high blood pressure."
            )
        })

    obesity_score = get_score("Obesity")

    if obesity_score is not None and obesity_score >= 60:
        diet.append({
            "title": "Supportive, balanced eating",
            "description": (
                "Focus on regular, balanced meals and a varied diet "
                "rather than restrictive eating or skipping meals. "
                "Individual nutrition needs differ."
            )
        })

    # --------------------------------------------------
    # 4. PHYSICAL ACTIVITY
    # --------------------------------------------------

    activity = get_number("physical_activity_minutes_per_week")

    if activity is not None:
        if activity < 150:
            lifestyle.append({
                "title": "Build regular movement",
                "description": (
                    "Your reported weekly activity is below "
                    "150 minutes. If appropriate for your abilities, "
                    "start with manageable activity and gradually "
                    "increase it. Suitable activity levels depend "
                    "on age and individual circumstances."
                )
            })
        else:
            lifestyle.append({
                "title": "Maintain regular activity",
                "description": (
                    "Maintain a consistent activity routine that "
                    "suits your abilities. Include enjoyable "
                    "activities and allow time for recovery."
                )
            })

    # --------------------------------------------------
    # 5. SLEEP
    # --------------------------------------------------

    sleep = get_number("sleep_hours_per_day")
    age = get_number("Age")

    if age is None:
        age = get_number("age")

    if sleep is not None:
        if sleep < 7:
            lifestyle.append({
                "title": "Review your sleep routine",
                "description": (
                    "Your reported sleep duration is under seven "
                    "hours. Consider a consistent sleep schedule "
                    "and enough time for rest. Sleep needs vary "
                    "with age, so this is general guidance."
                )
            })
        else:
            lifestyle.append({
                "title": "Maintain a consistent sleep schedule",
                "description": (
                    "Try to maintain regular sleep and wake times. "
                    "Adequate sleep duration and quality both matter."
                )
            })

    # --------------------------------------------------
    # 6. SCREEN TIME
    # --------------------------------------------------

    screen_time = get_number("screen_time_hours_per_day")

    if screen_time is not None and screen_time >= 6:
        lifestyle.append({
            "title": "Take regular screen breaks",
            "description": (
                "Your reported screen time is six hours or more "
                "per day. Consider regular breaks, stretching, "
                "changing position, and interrupting long periods "
                "of sitting where practical."
            )
        })

    # --------------------------------------------------
    # 7. SMOKING-RELATED GUIDANCE
    # --------------------------------------------------

    smoking = str(
        user_input.get("smoking_status", "")
    ).strip().lower()

    non_smoking_values = {
        "never",
        "no",
        "non-smoker",
        "nonsmoker",
        "never smoked",
        "not applicable"
    }

    if smoking and smoking not in non_smoking_values:
        lifestyle.append({
            "title": "Smoking cessation support",
            "description": (
                "If you currently smoke, a qualified healthcare "
                "professional or smoking cessation service can "
                "help you explore ways to quit."
            )
        })

    # --------------------------------------------------
    # 8. ALCOHOL-RELATED GUIDANCE
    # --------------------------------------------------

    alcohol = get_number("alcohol_consumption_per_week")

    if alcohol is not None and alcohol > 0:
        lifestyle.append({
            "title": "Review alcohol-related habits",
            "description": (
                "Consider discussing the health implications "
                "of alcohol consumption with a qualified "
                "healthcare professional, especially if you "
                "have health concerns or take medication."
            )
        })

    # --------------------------------------------------
    # 9. GENERAL WELLNESS TIPS
    # --------------------------------------------------

    general_tips.append({
        "title": "Make changes gradually",
        "description": (
            "Choose small, realistic habits you can maintain "
            "consistently rather than changing everything at once."
        )
    })

    general_tips.append({
        "title": "Stay hydrated",
        "description": (
            "Drink fluids regularly, adjusting your intake to "
            "your needs, activity, climate, and any medical advice."
        )
    })

    general_tips.append({
        "title": "Interpret scores carefully",
        "description": (
            "These five scores are generated by a model trained "
            "on a dataset. They are not verified probabilities "
            "of developing disease and cannot establish a diagnosis."
        )
    })

    general_tips.append({
        "title": "Seek professional guidance when needed",
        "description": (
            "Consult a qualified healthcare professional for "
            "personal health concerns, screening, or interpretation "
            "of actual measurements and laboratory results."
        )
    })

    # --------------------------------------------------
    # 10. RETURN ALL RECOMMENDATIONS
    # --------------------------------------------------

    return {
        "Diet Recommendations": diet,
        "Lifestyle Recommendations": lifestyle,
        "General Tips": general_tips
    }