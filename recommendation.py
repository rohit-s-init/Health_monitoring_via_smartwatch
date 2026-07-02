from typing import Dict, List


# ==========================================================
# Recommendation Engine
# ==========================================================

def generate_recommendations(
    lifestyle_risk: str,
    heart_risk: str = None,
    diabetes_risk: str = None
) -> Dict[str, List[str]]:

    recommendations = {

        "Exercise": [],

        "Diet": [],

        "Sleep": [],

        "Medical": []

    }

    # ======================================================
    # Lifestyle
    # ======================================================

    if lifestyle_risk == "High":

        recommendations["Exercise"].extend([

            "Walk at least 8,000–10,000 steps daily.",

            "Exercise for at least 45 minutes every day.",

            "Avoid prolonged sitting."

        ])

        recommendations["Sleep"].append(

            "Sleep for at least 7–8 hours every night."

        )

        recommendations["Diet"].append(

            "Maintain a balanced diet and healthy body weight."

        )

    elif lifestyle_risk == "Moderate":

        recommendations["Exercise"].append(

            "Increase daily physical activity."

        )

        recommendations["Sleep"].append(

            "Maintain a consistent sleep schedule."

        )

        recommendations["Diet"].append(

            "Eat a balanced diet."

        )

    else:

        recommendations["Exercise"].append(

            "Continue your current healthy lifestyle."

        )

    # ======================================================
    # Heart Disease
    # ======================================================

    if heart_risk == "High":

        recommendations["Medical"].extend([

            "Consult a cardiologist.",

            "Monitor blood pressure regularly."

        ])

        recommendations["Diet"].append(

            "Reduce sodium and saturated fat intake."

        )

        recommendations["Exercise"].append(

            "Perform moderate aerobic exercise after medical advice."

        )

    elif heart_risk == "Moderate":

        recommendations["Medical"].append(

            "Monitor blood pressure every week."

        )

        recommendations["Diet"].append(

            "Reduce salt intake."

        )

    # ======================================================
    # Diabetes
    # ======================================================

    if diabetes_risk == "High":

        recommendations["Medical"].append(

            "Consult an endocrinologist."

        )

        recommendations["Diet"].extend([

            "Reduce sugar intake.",

            "Avoid sugary beverages.",

            "Increase fibre-rich foods."

        ])

        recommendations["Exercise"].append(

            "Exercise at least 30 minutes daily."

        )

    elif diabetes_risk == "Moderate":

        recommendations["Diet"].append(

            "Reduce refined carbohydrates."

        )

        recommendations["Medical"].append(

            "Monitor blood glucose regularly."

        )

    # ======================================================
    # Remove Duplicate Recommendations
    # ======================================================

    for key in recommendations:

        recommendations[key] = list(

            dict.fromkeys(recommendations[key])

        )

    return recommendations


# ==========================================================
# Lifestyle Risk Weight
# ==========================================================

def lifestyle_score(risk):

    mapping = {

        "Low": 20,

        "Moderate": 50,

        "High": 80

    }

    return mapping.get(risk, 50)


# ==========================================================
# Overall Health Score
# ==========================================================

def overall_health_score(

    lifestyle_risk,

    heart_score=None,

    diabetes_score=None

):

    total_weight = 0

    weighted_sum = 0

    # Lifestyle (25%)

    weighted_sum += lifestyle_score(lifestyle_risk) * 0.25

    total_weight += 0.25

    # Heart (40%)

    if heart_score is not None:

        weighted_sum += heart_score * 0.40

        total_weight += 0.40

    # Diabetes (35%)

    if diabetes_score is not None:

        weighted_sum += diabetes_score * 0.35

        total_weight += 0.35

    average_risk = weighted_sum / total_weight

    health_score = 100 - average_risk

    return float(round(health_score, 2))


# ==========================================================
# Overall Health Status
# ==========================================================

def overall_status(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 60:
        return "Moderate"

    elif score >= 40:
        return "Needs Improvement"

    else:
        return "Critical"