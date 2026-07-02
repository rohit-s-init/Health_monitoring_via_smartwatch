import os
import joblib
from xgboost import XGBClassifier

# ==========================================================
# Model Directory
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")

# ==========================================================
# Lifestyle Model
# ==========================================================

lifestyle_model = XGBClassifier()

lifestyle_model.load_model(
    os.path.join(MODEL_DIR, "Lifestyle_Model.json")
)

lifestyle_encoders = joblib.load(
    os.path.join(MODEL_DIR, "Lifestyle_Encoders.pkl")
)

lifestyle_target_encoder = joblib.load(
    os.path.join(MODEL_DIR, "Lifestyle_Target_Encoder.pkl")
)

lifestyle_features = joblib.load(
    os.path.join(MODEL_DIR, "Lifestyle_Features.pkl")
)

# ==========================================================
# Heart Model
# ==========================================================

heart_model = joblib.load(
    os.path.join(MODEL_DIR, "Heart_Model.pkl")
)

heart_features = joblib.load(
    os.path.join(MODEL_DIR, "Heart_Features.pkl")
)

# ==========================================================
# Diabetes Model
# ==========================================================

diabetes_model = joblib.load(
    os.path.join(MODEL_DIR, "Diabetes_Model.pkl")
)

diabetes_encoders = joblib.load(
    os.path.join(MODEL_DIR, "Diabetes_Encoders.pkl")
)

diabetes_features = joblib.load(
    os.path.join(MODEL_DIR, "Diabetes_Features.pkl")
)

# ==========================================================
# Check Models
# ==========================================================

print("===================================")
print("Models Loaded Successfully")
print("===================================")

print("✓ Lifestyle Model")
print("✓ Heart Model")
print("✓ Diabetes Model")