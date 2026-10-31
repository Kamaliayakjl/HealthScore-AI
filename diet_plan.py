def generate_diet_plan(user_input, risk_scores):
    """Generate personalized educational meal suggestions."""

    import math
    import re

    user_input = user_input or {}
    risk_scores = risk_scores or {}

    # --------------------------------------------------
    # 1. HELPER FUNCTIONS
    # --------------------------------------------------

    def get_text(key, default=""):
        value = user_input.get(key, default)
        return default if value is None else str(value).strip()

    def get_number(key):
        try:
            number = float(user_input.get(key))
            return number if math.isfinite(number) else None
        except (TypeError, ValueError):
            return None

    def get_score(*keys):
        for key in keys:
            try:
                value = risk_scores.get(key)
                if value is not None:
                    number = float(value)
                    if math.isfinite(number):
                        return number
            except (TypeError, ValueError):
                pass
        return None

    def split_terms(value):
        if not value:
            return []

        return [
            item.strip().lower()
            for item in re.split(r"[,;]", value)
            if item.strip()
        ]

    def normalize_text(value):
        value = str(value or "").strip().lower()
        value = value.replace("_", "-")
        return " ".join(value.split())

    # --------------------------------------------------
    # 2. READ AND NORMALIZE PREFERENCES
    # --------------------------------------------------

    diet_preference = normalize_text(
        get_text("dietary_preference", "Vegetarian")
    )

    diet_aliases = {
        "vegetarian": "vegetarian",
        "veg": "vegetarian",
        "lacto-vegetarian": "vegetarian",
        "ovo-vegetarian": "vegetarian",
        "non-vegetarian": "non-vegetarian",
        "non vegetarian": "non-vegetarian",
        "non-veg": "non-vegetarian",
        "non veg": "non-vegetarian",
        "nonveg": "non-vegetarian",
        "omnivore": "non-vegetarian",
        "everything": "non-vegetarian",
        "vegan": "vegan",
    }

    # Unknown values safely default to vegetarian.
    diet_preference = diet_aliases.get(
        diet_preference, "vegetarian"
    )

    vegetarian_only = diet_preference == "vegetarian"
    vegan_only = diet_preference == "vegan"
    non_vegetarian = diet_preference == "non-vegetarian"

    budget = normalize_text(
        get_text("food_budget", "Moderate")
    )

    cooking_time = normalize_text(
        get_text("cooking_time", "Moderate")
    )

    liked_foods = split_terms(get_text("liked_foods", ""))
    allergies = split_terms(get_text("food_allergies", ""))
    foods_to_avoid = split_terms(get_text("foods_to_avoid", ""))

    activity = get_number("physical_activity_minutes_per_week")
    sleep = get_number("sleep_hours_per_day")

    # --------------------------------------------------
    # 3. MEAL DATABASE
    # --------------------------------------------------

    meals = {
        "Breakfast": [
            {
                "name": "Vegetable poha",
                "tags": ["rice", "vegetables", "peanuts"],
                "budget": "low", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Vegetable oats",
                "tags": ["oats", "vegetables"],
                "budget": "low", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Besan chilla with vegetables",
                "tags": ["chickpeas", "besan", "vegetables"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Idli with sambar",
                "tags": ["rice", "lentils"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Curd with fruit and oats",
                "tags": ["dairy", "curd", "milk", "fruit", "oats"],
                "budget": "moderate", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Vegetable omelette with whole-wheat toast",
                "tags": ["eggs", "vegetables", "wheat"],
                "budget": "moderate", "time": "quick",
                "diet": "egg",
            },
            {
                "name": "Boiled eggs with whole-wheat toast",
                "tags": ["eggs", "wheat"],
                "budget": "moderate", "time": "quick",
                "diet": "egg",
            },
            {
                "name": "Tofu and vegetable sandwich",
                "tags": ["soy", "tofu", "wheat", "vegetables"],
                "budget": "moderate", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Paneer bhurji with roti",
                "tags": ["dairy", "paneer", "milk", "wheat"],
                "budget": "moderate", "time": "moderate",
                "diet": "vegetarian",
            },
        ],

        "Lunch": [
            {
                "name": "Roti, dal and seasonal vegetables",
                "tags": ["wheat", "lentils", "vegetables"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Rice with rajma and vegetables",
                "tags": ["rice", "kidney beans", "vegetables"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Chickpea and vegetable rice bowl",
                "tags": ["chickpeas", "rice", "vegetables"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Vegetable pulao with raita",
                "tags": ["rice", "vegetables", "dairy", "curd", "milk"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Paneer with roti and vegetables",
                "tags": ["dairy", "paneer", "milk", "wheat", "vegetables"],
                "budget": "moderate", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Egg curry with rice and vegetables",
                "tags": ["eggs", "rice", "vegetables"],
                "budget": "moderate", "time": "moderate",
                "diet": "egg",
            },
            {
                "name": "Chicken with rice and vegetables",
                "tags": ["chicken", "meat", "rice", "vegetables"],
                "budget": "high", "time": "moderate",
                "diet": "non-vegetarian",
            },
            {
                "name": "Fish with rice and vegetables",
                "tags": ["fish", "seafood", "rice", "vegetables"],
                "budget": "high", "time": "moderate",
                "diet": "non-vegetarian",
            },
            {
                "name": "Chicken roti wrap with vegetables",
                "tags": ["chicken", "meat", "wheat", "vegetables"],
                "budget": "high", "time": "moderate",
                "diet": "non-vegetarian",
            },
        ],

        "Evening Snack": [
            {
                "name": "Seasonal fruit",
                "tags": ["fruit"],
                "budget": "low", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Roasted chana",
                "tags": ["chickpeas"],
                "budget": "low", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Cucumber and carrot sticks",
                "tags": ["vegetables"],
                "budget": "low", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Curd with fruit",
                "tags": ["dairy", "curd", "milk", "fruit"],
                "budget": "moderate", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Nuts and seeds",
                "tags": ["nuts", "seeds"],
                "budget": "moderate", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Boiled egg",
                "tags": ["eggs"],
                "budget": "moderate", "time": "quick",
                "diet": "egg",
            },
            {
                "name": "Hummus with vegetable sticks",
                "tags": ["chickpeas", "sesame", "vegetables"],
                "budget": "moderate", "time": "quick",
                "diet": "vegetarian",
            },
        ],

        "Dinner": [
            {
                "name": "Vegetable khichdi",
                "tags": ["rice", "lentils", "vegetables"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Roti, dal and cooked vegetables",
                "tags": ["wheat", "lentils", "vegetables"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Chickpea and vegetable bowl",
                "tags": ["chickpeas", "vegetables"],
                "budget": "low", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Vegetable soup with whole-wheat toast",
                "tags": ["vegetables", "wheat"],
                "budget": "low", "time": "quick",
                "diet": "vegetarian",
            },
            {
                "name": "Paneer with vegetables and roti",
                "tags": ["dairy", "paneer", "milk", "vegetables", "wheat"],
                "budget": "moderate", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Tofu with rice and vegetables",
                "tags": ["soy", "tofu", "rice", "vegetables"],
                "budget": "moderate", "time": "moderate",
                "diet": "vegetarian",
            },
            {
                "name": "Egg bhurji with roti and vegetables",
                "tags": ["eggs", "wheat", "vegetables"],
                "budget": "moderate", "time": "moderate",
                "diet": "egg",
            },
            {
                "name": "Chicken with vegetables and rice",
                "tags": ["chicken", "meat", "vegetables", "rice"],
                "budget": "high", "time": "moderate",
                "diet": "non-vegetarian",
            },
            {
                "name": "Fish with vegetables and rice",
                "tags": ["fish", "seafood", "vegetables", "rice"],
                "budget": "high", "time": "moderate",
                "diet": "non-vegetarian",
            },
        ],
    }

    # --------------------------------------------------
    # 4. FILTER BY DIETARY PREFERENCE
    # --------------------------------------------------

    vegan_forbidden_tags = {
        "dairy", "curd", "paneer", "milk", "yogurt", "eggs"
    }

    for meal_type in meals:
        filtered = []

        for meal in meals[meal_type]:
            meal_diet = meal["diet"]
            tags = set(meal["tags"])

            if vegan_only:
                if meal_diet != "vegetarian":
                    continue

                if tags & vegan_forbidden_tags:
                    continue

            elif vegetarian_only:
                if meal_diet != "vegetarian":
                    continue

            # Non-vegetarian users can receive all three
            # categories, subject to other filters.

            filtered.append(meal)

        meals[meal_type] = filtered

    # --------------------------------------------------
    # 5. FILTER ALLERGIES AND FOODS TO AVOID
    # --------------------------------------------------

    allergen_groups = {
        "peanut": {"peanuts"},
        "peanuts": {"peanuts"},
        "groundnut": {"peanuts"},
        "milk": {"dairy", "curd", "paneer", "milk", "yogurt"},
        "dairy": {"dairy", "curd", "paneer", "milk", "yogurt"},
        "lactose": {"dairy", "curd", "paneer", "milk", "yogurt"},
        "soy": {"soy", "tofu"},
        "soya": {"soy", "tofu"},
        "gluten": {"wheat"},
        "wheat": {"wheat"},
        "egg": {"eggs"},
        "eggs": {"eggs"},
        "fish": {"fish", "seafood"},
        "seafood": {"fish", "seafood"},
        "shellfish": {"seafood"},
        "nuts": {"nuts"},
        "tree nuts": {"nuts"},
        "chickpea": {"chickpeas", "besan"},
        "chickpeas": {"chickpeas", "besan"},
        "sesame": {"sesame"},
        "chicken": {"chicken", "meat"},
        "meat": {"chicken", "meat"},
    }

    forbidden_tags = set()

    for term in allergies + foods_to_avoid:
        forbidden_tags.add(term)

        if term in allergen_groups:
            forbidden_tags.update(allergen_groups[term])

    # Normalize known aliases into the tags used by the database.
    tag_aliases = {
        "peanut": "peanuts",
        "groundnut": "peanuts",
        "soya": "soy",
        "egg": "eggs",
        "chickpea": "chickpeas",
    }

    forbidden_tags = {
        tag_aliases.get(tag, tag)
        for tag in forbidden_tags
    }

    def meal_matches_forbidden_tag(meal):
        tags = set(meal["tags"])
        name = meal["name"].lower()

        for forbidden in forbidden_tags:
            if forbidden in tags:
                return True

            # Match a food name as a whole word, not an arbitrary
            # substring of an unrelated word.
            if re.search(
                r"\b" + re.escape(forbidden) + r"\b",
                name
            ):
                return True

        return False

    for meal_type in meals:
        meals[meal_type] = [
            meal for meal in meals[meal_type]
            if not meal_matches_forbidden_tag(meal)
        ]

    # --------------------------------------------------
    # 6. FILTER BY BUDGET AND COOKING TIME
    # --------------------------------------------------

    if any(word in budget for word in ["low", "budget", "cheap"]):
        allowed_budgets = {"low"}
    elif "high" in budget:
        allowed_budgets = {"low", "moderate", "high"}
    else:
        allowed_budgets = {"low", "moderate"}

    # First try the requested budget. If a meal category becomes
    # empty, relax only the budget constraint for that category.
    for meal_type in meals:
        budget_filtered = [
            meal for meal in meals[meal_type]
            if meal["budget"] in allowed_budgets
        ]

        if budget_filtered:
            meals[meal_type] = budget_filtered

    quick_only = any(
        word in cooking_time
        for word in ["quick", "15", "10", "little"]
    )

    if quick_only:
        for meal_type in meals:
            quick_meals = [
                meal for meal in meals[meal_type]
                if meal["time"] == "quick"
            ]

            # Relax cooking-time filtering for a category if no
            # quick meal survives. Never relax allergy filters.
            if quick_meals:
                meals[meal_type] = quick_meals

    # --------------------------------------------------
    # 7. SELECT PERSONALIZED MEALS
    # --------------------------------------------------

    selected_plan = {}

    def preference_score(meal):
        searchable = (
            meal["name"] + " " + " ".join(meal["tags"])
        ).lower()

        liked_score = sum(
            1 for term in liked_foods
            if term in searchable
        )

        if non_vegetarian:
            if meal["diet"] == "non-vegetarian":
                diet_priority = 3
            elif meal["diet"] == "egg":
                diet_priority = 2
            else:
                diet_priority = 1
        else:
            diet_priority = 1

        return diet_priority, liked_score

    for meal_type, options in meals.items():
        if not options:
            selected_plan[meal_type] = [
                "No matching meal found for your current filters. "
                "Try adjusting your budget, cooking time, or exclusions."
            ]
            continue

        options = sorted(
            options,
            key=preference_score,
            reverse=True,
        )

        selected_plan[meal_type] = [
            meal["name"] for meal in options[:3]
        ]

    # --------------------------------------------------
    # 8. PERSONALIZED EDUCATIONAL NOTES
    # --------------------------------------------------

    notes = [
        "These are educational meal suggestions, not a medical diet prescription.",
        "Meal portions should be adapted to individual needs.",
        "Check ingredient labels and cross-contamination risks carefully when allergies are present.",
        f"Selected dietary preference: {diet_preference.title()}.",
    ]

    diabetes = get_score("Diabetes", "diabetes_risk_score")
    cholesterol = get_score("Cholesterol", "cholesterol_risk_score")
    hypertension = get_score("Hypertension", "hypertension_risk_score")
    heart = get_score("Heart Disease", "heart_disease_risk_score")
    obesity = get_score("Obesity", "obesity_risk_score")

    # Demonstration threshold for this college project only.
    if diabetes is not None and diabetes >= 60:
        notes.append(
            "Diabetes-related educational focus: consider balanced "
            "meals, fibre-rich foods and unsweetened drinks. "
            "The model score is not a diagnosis."
        )

    if cholesterol is not None and cholesterol >= 60:
        notes.append(
            "Cholesterol-related educational focus: consider "
            "fibre-rich foods such as oats, beans, fruit and lentils."
        )

    if hypertension is not None and hypertension >= 60:
        notes.append(
            "Blood-pressure educational focus: consider limiting "
            "excessive sodium and frequently eating highly salted foods."
        )

    if heart is not None and heart >= 60:
        notes.append(
            "Heart-health educational focus: consider a varied diet "
            "with vegetables, fruit, whole grains and appropriate "
            "sources of unsaturated fats."
        )

    if obesity is not None and obesity >= 60:
        notes.append(
            "General nutrition focus: aim for regular, balanced meals "
            "rather than restrictive eating or skipping meals."
        )

    if activity is not None and activity < 150:
        notes.append(
            "Your reported activity is below 150 minutes per week. "
            "Consider gradually building movement appropriate to "
            "your age and circumstances."
        )

    if sleep is not None and sleep < 7:
        notes.append(
            "Your reported sleep is under 7 hours. Sleep needs vary "
            "by age; consider reviewing your sleep routine."
        )

    if not any(
        score is not None and score >= 60
        for score in [
            diabetes, cholesterol, hypertension, heart, obesity
        ]
    ):
        notes.append(
            "No score-based notes were triggered by the project's "
            "demonstration threshold. This does not mean health risks "
            "are absent."
        )

    # --------------------------------------------------
    # 9. RETURN RESULTS TO THE APP
    # --------------------------------------------------

    return {
        "meal_plan": selected_plan,
        "notes": notes,
        "preferences_used": {
            "dietary_preference": diet_preference.title(),
            "budget": budget,
            "cooking_time": cooking_time,
            "liked_foods": ", ".join(liked_foods),
            "food_allergies": ", ".join(allergies),
            "foods_to_avoid": ", ".join(foods_to_avoid),
        },
    }