from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from test import assign_burnout_risk
import joblib

app = FastAPI(title="Burnout Risk API")

# Load the saved models
scaler = joblib.load('./trained_models/scaler.pkl')
pca = joblib.load('./trained_models/pca.pkl')
min_max_scaler = joblib.load('./trained_models/min_max_scaler.pkl')
kmeans = joblib.load('./trained_models/kmeans.pkl')
iso_forest = joblib.load('./trained_models/iso_forest.pkl')

# Define request schema


class FlourishingScale(BaseModel):
    ques1: int
    ques2: int
    ques3: int
    ques4: int
    ques5: int
    ques6: int
    ques7: int
    ques8: int


@app.get("/")
def home():
    return {"message": "Welcome to the Burnout Risk API!"}


@app.post("/calculate")
def calculate_risk(data: FlourishingScale):
    input_data = np.array([data.ques1, data.ques2, data.ques3,
                          data.ques4, data.ques5, data.ques6, data.ques7, data.ques8])
    risk_score = assign_burnout_risk(
        input_data, scaler, pca, kmeans, iso_forest, min_max_scaler)

    return {"risk_score": float(risk_score)}
