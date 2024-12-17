import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np 
import logging
from typing import List
from src.models.predict import make_predictions
from src.utils.config import Config
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Load model and features
model_path = "models/random_forest.pkl"
feature_path = "models/features.json"
with open(feature_path, "r") as f:
    feature_names = json.load(f).get("feature_names", [])

EXPECTED_FEATURES = feature_names  # Assuming features are listed in the JSON file


def preprocess_input(data: List[dict], expected_features: List[str]):
    logging.info("Starting input preprocessing.")
    input_df = pd.DataFrame(data)

    # Convert 'TotalCharges' to numeric and handle missing values
    input_df["TotalCharges"] = pd.to_numeric(input_df["TotalCharges"], errors="coerce").fillna(0)

    # One-hot encode categorical columns
    input_df = pd.get_dummies(input_df)

    # Add missing columns with default value 0
    for feature in expected_features:
        if feature not in input_df.columns:
            input_df[feature] = 0

    # Reorder columns to match model training data
    input_df = input_df[expected_features]

    logging.info("Input preprocessing completed successfully.")
    return input_df

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Churn Model"}

@app.post("/predict")
def predict(data: List[dict]):
    try:
        logging.info("Received prediction request.")
        logging.info(f"Raw input: {data}")

        # Preprocess input data
        input_data = preprocess_input(data, EXPECTED_FEATURES)

        # Make predictions
        logging.info("Loading the trained model and making predictions.")
        predictions = make_predictions(input_data, Config.MODEL_PATH)
        logging.info(f"Raw predictions: {predictions}, Type: {type(predictions)}")

        # Ensure predictions are converted to native Python types
        predictions = predictions.tolist() if isinstance(predictions, (np.ndarray, pd.Series)) else predictions
        predictions = [int(pred) for pred in predictions]  # Convert to a list of Python integers

        # Format response
        response = {"predictions": predictions}
        logging.info("Prediction successful.")
        return response

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during prediction.")

