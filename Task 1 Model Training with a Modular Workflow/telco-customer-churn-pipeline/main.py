import logging
from src.data.data_ingestion import load_data
from src.data.preprocessing import preprocess_data
from src.models.train import train_model
from src.utils.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    try:
        logging.info("Starting main workflow...")

        # Load data
        data = load_data(Config.RAW_DATA_PATH)

        # Preprocess data
        processed_data = preprocess_data(data)

        # Train model
        train_model(processed_data, Config.TARGET_COLUMN, Config.MODEL_PATH)

        logging.info("Workflow completed successfully!")
    except Exception as e:
        logging.error(f"Error in main workflow: {e}")
