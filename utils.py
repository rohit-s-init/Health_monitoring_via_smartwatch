from fastapi import HTTPException
import pandas as pd


# ==========================================================
# BMI Calculator
# ==========================================================

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """
    Calculate BMI from height and weight.
    """

    if height_cm <= 0:
        raise HTTPException(
            status_code=400,
            detail="Height must be greater than 0."
        )

    bmi = weight_kg / ((height_cm / 100) ** 2)

    return round(bmi, 2)


# ==========================================================
# Arrange Features
# ==========================================================

def arrange_features(df: pd.DataFrame, feature_order: list):

    """
    Rearrange dataframe columns exactly as used during training.
    """

    missing = []

    for feature in feature_order:

        if feature not in df.columns:
            missing.append(feature)

    if len(missing) > 0:

        raise HTTPException(

            status_code=500,

            detail=f"Missing features : {missing}"

        )

    return df[feature_order]


# ==========================================================
# Safe Label Encoding
# ==========================================================

def safe_encode(value, encoder, field_name):

    """
    Encode categorical values safely.
    """

    classes = list(encoder.classes_)

    if value not in classes:

        raise HTTPException(

            status_code=400,

            detail=f"Invalid value '{value}' for '{field_name}'. "
                   f"Allowed values : {classes}"

        )

    return encoder.transform([value])[0]


# ==========================================================
# Probability Percentage
# ==========================================================

def probability_percentage(probability):

    """
    Convert probability to percentage.
    """

    return float(round(float(probability) * 100, 2))


# ==========================================================
# Heart Risk Level
# ==========================================================

def heart_risk_level(score):

    if score < 30:
        return "Low"

    elif score < 70:
        return "Moderate"

    return "High"


# ==========================================================
# Diabetes Risk Level
# ==========================================================

def diabetes_risk_level(score):

    if score < 30:
        return "Low"

    elif score < 70:
        return "Moderate"

    return "High"


# ==========================================================
# Lifestyle Weight
# ==========================================================

def lifestyle_weight(risk):

    """
    Used for Overall Health Score.
    """

    mapping = {

        "Low": 20,

        "Moderate": 50,

        "High": 80

    }

    return mapping.get(risk, 50)


# ==========================================================
# Overall Health Score
# ==========================================================

def calculate_health_score(

    lifestyle_risk,

    heart_score=None,

    diabetes_score=None

):

    lifestyle_score = lifestyle_weight(lifestyle_risk)

    weighted_sum = lifestyle_score * 0.25

    total_weight = 0.25

    if heart_score is not None:

        weighted_sum += heart_score * 0.40

        total_weight += 0.40

    if diabetes_score is not None:

        weighted_sum += diabetes_score * 0.35

        total_weight += 0.35

    weighted_average = weighted_sum / total_weight

    overall = 100 - weighted_average

    return round(overall, 2)


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

    return "Critical"