from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    LifestyleInput,
    FullHealthInput
)

from predict import (
    predict_lifestyle,
    predict_heart,
    predict_diabetes
)

from recommendation import (
    generate_recommendations,
    overall_health_score,
    overall_status
)

# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(

    title="SmartWatch AI Health Monitoring API",

    version="2.0.0",

    description="AI Powered SmartWatch Health Monitoring & Early Disease Prediction"

)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():

    return {

        "message": "SmartWatch AI Backend Running",

        "version": "2.0.0"

    }

# ==========================================================
# Lifestyle Prediction
# ==========================================================

@app.post("/predict/lifestyle")
def lifestyle_prediction(data: LifestyleInput):

    return predict_lifestyle(data)

# ==========================================================
# Full Health Assessment
# ==========================================================

@app.post("/predict/full-health")
def full_health_prediction(data: FullHealthInput):

    # ------------------------------------------------------
    # Lifestyle Prediction (Always Runs)
    # ------------------------------------------------------

    lifestyle = predict_lifestyle(data)

    # ------------------------------------------------------
    # Heart Prediction (Optional)
    # ------------------------------------------------------

    heart = None

    if (

        data.ap_hi is not None

        and data.ap_lo is not None

        and data.cholesterol is not None

        and data.gluc is not None

        and data.smoke is not None

        and data.alco is not None

        and data.active is not None

    ):

        heart = predict_heart(data)

    # ------------------------------------------------------
    # Diabetes Prediction (Optional)
    # ------------------------------------------------------

    diabetes = None

    if (

        data.hypertension is not None

        and data.heart_disease is not None

        and data.smoking_history is not None

        and data.HbA1c_level is not None

        and data.blood_glucose_level is not None

    ):

        diabetes = predict_diabetes(data)

    # ------------------------------------------------------
    # Overall Health Score
    # ------------------------------------------------------

    heart_score = None

    diabetes_score = None

    if heart is not None:

        heart_score = heart["RiskScore"]

    if diabetes is not None:

        diabetes_score = diabetes["RiskScore"]

    health_score = overall_health_score(

        lifestyle["Risk"],

        heart_score,

        diabetes_score

    )

    health_status = overall_status(

        health_score

    )

    # ------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------

    recommendations = generate_recommendations(

        lifestyle["Risk"],

        heart["Risk"] if heart else None,

        diabetes["Risk"] if diabetes else None

    )
    

    # ------------------------------------------------------
    # Final Response
    # ------------------------------------------------------

    return {

        "HealthSummary": {

            "OverallHealthScore": float(health_score),

            "OverallStatus": health_status

        },

        "Lifestyle": lifestyle,

        "Heart": heart,

        "Diabetes": diabetes,

        "Recommendations": recommendations

    }
@app.get("/debug/model-info")
def model_info():
    return {
        "LifestyleFeatures": lifestyle_features,
        "GenderClasses": list(lifestyle_encoders["Gender"].classes_),
        "WorkoutClasses": list(lifestyle_encoders["Workout_Type"].classes_),
        "ActivityClasses": list(lifestyle_encoders["Activity_Status"].classes_)
    }