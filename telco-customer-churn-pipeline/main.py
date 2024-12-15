import logging
from src.data.data_ingestion import load_data
from src.data.preprocessing import preprocess_data
from src.models.train import train_model
from src.models.predict import make_predictions
from src.utils.config import Config
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    try:
        logging.info("Starting main workflow...")

        # Step 1: Load the data
        data = load_data(Config.RAW_DATA_PATH)

        # Step 2: Preprocess the data
        features, target = preprocess_data(data)

        # Step 3: Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        logging.info("Data split into training and testing sets.")
        
        # Step 4: Train the model using the training set
        train_model(X_train, y_train, Config.MODEL_PATH)
        

        # Step 5: Make predictions on the training data (or test data if provided)
        predictions = make_predictions(X_test, Config.MODEL_PATH)
        
        # Use metrics like accuracy_score, f1_score, etc. from sklearn
        
        accuracy = accuracy_score(y_test, predictions)
        logging.info(f"Model accuracy on the testing set: {accuracy}")
        

        # Log predictions (for verification purposes, you may want to save these elsewhere)
        logging.info(f"Sample predictions: {predictions[:5]}")

        logging.info("Workflow completed successfully!")

    except Exception as e:
        logging.error(f"Error in main workflow: {e}")
