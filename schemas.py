from pydantic import BaseModel, Field
from typing import Optional


# ==========================================================
# Lifestyle Model Input
# ==========================================================

class LifestyleInput(BaseModel):

    Age: int = Field(..., ge=1, le=120)

    Gender: str

    Height_cm: float = Field(..., gt=50, le=250)

    Weight_kg: float = Field(..., gt=10, le=300)

    Heart_Rate_bpm: int = Field(..., ge=30, le=220)

    Blood_Oxygen: int = Field(..., ge=50, le=100)

    Step_Count: int = Field(..., ge=0)

    Calories_Burned: int = Field(..., ge=0)

    Hours_Slept: float = Field(..., ge=0, le=24)

    Active_Minutes: int = Field(..., ge=0, le=1440)

    Workout_Type: str

    Activity_Status: str


# ==========================================================
# Heart Disease Optional Input
# ==========================================================

class HeartInput(BaseModel):

    ap_hi: Optional[int] = Field(None, ge=60, le=250)

    ap_lo: Optional[int] = Field(None, ge=40, le=180)

    cholesterol: Optional[int] = Field(
        None,
        ge=1,
        le=3
    )

    gluc: Optional[int] = Field(
        None,
        ge=1,
        le=3
    )

    smoke: Optional[int] = Field(
        None,
        ge=0,
        le=1
    )

    alco: Optional[int] = Field(
        None,
        ge=0,
        le=1
    )

    active: Optional[int] = Field(
        None,
        ge=0,
        le=1
    )


# ==========================================================
# Diabetes Optional Input
# ==========================================================

class DiabetesInput(BaseModel):

    hypertension: Optional[int] = Field(
        None,
        ge=0,
        le=1
    )

    heart_disease: Optional[int] = Field(
        None,
        ge=0,
        le=1
    )

    smoking_history: Optional[str] = None

    HbA1c_level: Optional[float] = Field(
        None,
        ge=3,
        le=20
    )

    blood_glucose_level: Optional[int] = Field(
        None,
        ge=40,
        le=500
    )


# ==========================================================
# Complete Health Input
# ==========================================================

class FullHealthInput(

    LifestyleInput,

    HeartInput,

    DiabetesInput

):
    """
    Complete Health Assessment Request

    Lifestyle data is mandatory.

    Heart and Diabetes parameters are optional.

    If optional fields are missing,
    only Lifestyle prediction will be performed.
    """

    pass