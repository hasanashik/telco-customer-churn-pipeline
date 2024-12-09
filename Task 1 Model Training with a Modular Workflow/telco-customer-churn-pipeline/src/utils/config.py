import os


class Config:
    RAW_DATA_PATH = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    PROCESSED_DATA_PATH = "data/processed/processed_data.csv"
    MODEL_PATH = "models/random_forest.pkl"
    LOG_FILE = "logs/project.log"
    TARGET_COLUMN = "Churn"
