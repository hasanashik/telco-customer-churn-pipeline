import logging
import pandas as pd
from src.models.predict import make_predictions
from src.utils.config import Config
from src.data.data_ingestion import load_data
from src.data.preprocessing import preprocess_data  # Import preprocessing

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    try:
        logging.info("Loading test data...")
        data = load_data(Config.RAW_DATA_PATH)

        # Preprocess the data
        logging.info("Preprocessing the test data...")
        processed_data = preprocess_data(data,False)

        # Drop the target column if present
        if Config.TARGET_COLUMN in processed_data.columns:
            processed_data = processed_data.drop(
                columns=[Config.TARGET_COLUMN])

        logging.info("Testing the prediction function...")
        predictions = make_predictions(processed_data, Config.MODEL_PATH)
        print("Predictions:", predictions)

        prediction_labels = ["No Churn" if pred ==
                             0 else "Churn" for pred in predictions]
        print("Prediction Labels:", prediction_labels)

    except Exception as e:
        logging.error(f"Error in testing: {e}")
