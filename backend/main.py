from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title="Customer Churn Prediction API")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "churn_pipeline.pkl")
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Model not found at {MODEL_PATH}. Run train_model.py first.")

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.post("/predict")
def predict_churn(data: CustomerData):
    try:
        # Convert request to DataFrame
        df = pd.DataFrame([data.model_dump()])
        
        # Make Prediction
        probability = model.predict_proba(df)[0][1]
        prediction = int(model.predict(df)[0])
        
        risk_level = "High Risk" if probability > 0.6 else "Medium Risk" if probability > 0.3 else "Low Risk"

        return {
            "churn": bool(prediction),
            "probability": round(probability * 100, 2),
            "risk_level": risk_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
