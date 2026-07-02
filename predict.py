import pandas as pd
from fastapi import HTTPException

from model_loader import (
    lifestyle_model,
    lifestyle_encoders,
    lifestyle_target_encoder,
    lifestyle_features,
    heart_model,
    heart_features,
)

from utils import (
    calculate_bmi,
    arrange_features,
    probability_percentage,
    heart_risk_level,
    safe_encode,
)


# ==========================================================
# Gender Mapping (Heart Dataset)
# ==========================================================

GENDER_MAP = {
    "Male": 2,
    "Female": 1
}


# ==========================================================
# Lifestyle Prediction
# ==========================================================

def predict_lifestyle(data):
    """
    Lifestyle Prediction

    Output:
    {
        "Risk":"Low"
    }
    """

    try:

        bmi = calculate_bmi(
            data.Height_cm,
            data.Weight_kg
        )

        sample = {

            "Age": data.Age,

            "Gender": data.Gender,

            "Height (cm)": data.Height_cm,

            "Weight (kg)": data.Weight_kg,

            "Heart_Rate (bpm)": data.Heart_Rate_bpm,

            "Blood_Oxygen": data.Blood_Oxygen,

            "Step_Count": data.Step_Count,

            "Calories_Burned": data.Calories_Burned,

            "Hours_Slept": data.Hours_Slept,

            "Active_Minutes": data.Active_Minutes,

            "Workout_Type": data.Workout_Type,

            "Activity_Status": data.Activity_Status,

            "BMI": bmi

        }

        df = pd.DataFrame([sample])

        # ---------------------------------------------
        # Safe Encoding
        # ---------------------------------------------

        df["Gender"] = safe_encode(
            data.Gender,
            lifestyle_encoders["Gender"],
            "Gender"
        )

        df["Workout_Type"] = safe_encode(
            data.Workout_Type,
            lifestyle_encoders["Workout_Type"],
            "Workout_Type"
        )

        df["Activity_Status"] = safe_encode(
            data.Activity_Status,
            lifestyle_encoders["Activity_Status"],
            "Activity_Status"
        )

        # ---------------------------------------------
        # Arrange Features
        # ---------------------------------------------

        df = arrange_features(
            df,
            lifestyle_features
        )

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        prediction = lifestyle_model.predict(df)

        prediction = lifestyle_target_encoder.inverse_transform(
            prediction
        )

        return {

            "Risk": prediction[0]

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Lifestyle Prediction Error : {str(e)}"

        )


# ==========================================================
# Heart Disease Prediction
# ==========================================================

def predict_heart(data):
    """
    Heart Disease Prediction

    Output

    {
        "Risk":"Moderate",
        "RiskScore":62.81
    }
    """

    try:

        bmi = calculate_bmi(
            data.Height_cm,
            data.Weight_kg
        )

        sample = {

            "age": data.Age,

            "gender": GENDER_MAP[data.Gender],

            "height": data.Height_cm,

            "weight": data.Weight_kg,

            "ap_hi": data.ap_hi,

            "ap_lo": data.ap_lo,

            "cholesterol": data.cholesterol,

            "gluc": data.gluc,

            "smoke": data.smoke,

            "alco": data.alco,

            "active": data.active,

            "BMI": bmi

        }

        df = pd.DataFrame([sample])

        # ---------------------------------------------
        # Arrange Features
        # ---------------------------------------------

        df = arrange_features(
            df,
            heart_features
        )

        # ---------------------------------------------
        # Predict
        # ---------------------------------------------

        probability = heart_model.predict_proba(df)

        risk_score = float(probability_percentage(

            probability[0][1]

        ))

        risk_level = heart_risk_level(

            risk_score

        )

        return {

            "Risk": risk_level,

            "RiskScore": risk_score

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Heart Prediction Error : {str(e)}"

        )
    # ==========================================================
# Diabetes Prediction
# ==========================================================

from model_loader import (
    diabetes_model,
    diabetes_encoders,
    diabetes_features
)

from utils import (
    diabetes_risk_level
)


def predict_diabetes(data):
    """
    Diabetes Prediction

    Returns

    {
        "Risk":"Moderate",
        "RiskScore":58.71
    }
    """

    try:

        bmi = calculate_bmi(
            data.Height_cm,
            data.Weight_kg
        )

        sample = {

            "gender": data.Gender,

            "age": data.Age,

            "hypertension": data.hypertension,

            "heart_disease": data.heart_disease,

            "smoking_history": data.smoking_history,

            "bmi": bmi,

            "HbA1c_level": data.HbA1c_level,

            "blood_glucose_level": data.blood_glucose_level

        }

        df = pd.DataFrame([sample])

        # --------------------------------------------
        # Encode Gender
        # --------------------------------------------

        df["gender"] = safe_encode(

            data.Gender,

            diabetes_encoders["gender"],

            "gender"

        )

        # --------------------------------------------
        # Encode Smoking History
        # --------------------------------------------

        df["smoking_history"] = safe_encode(

            data.smoking_history,

            diabetes_encoders["smoking_history"],

            "smoking_history"

        )

        # --------------------------------------------
        # Arrange Features
        # --------------------------------------------

        df = arrange_features(

            df,

            diabetes_features

        )

        # --------------------------------------------
        # Predict
        # --------------------------------------------

        probability = diabetes_model.predict_proba(df)

        risk_score = float(probability_percentage(
            probability[0][1]
        ))

        risk_level = diabetes_risk_level(
            risk_score
        )

        return {

            "Risk": risk_level,

            "RiskScore": risk_score

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Diabetes Prediction Error : {str(e)}"

        )