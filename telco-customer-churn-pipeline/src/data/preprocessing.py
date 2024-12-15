import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import logging
import joblib
import json
from src.utils.config import Config

def preprocess_data(df: pd.DataFrame, is_training: bool = True) -> tuple:
    """
    Preprocess data for model training or inference.

    Steps:
        - Drop irrelevant columns (e.g., 'customerID').
        - Handle missing values.
        - Encode categorical variables.
        - Scale numerical features.

    Args:
        df (pd.DataFrame): Input DataFrame.
        is_training (bool): Whether it's for training or inference.

    Returns:
        tuple: Processed features (pd.DataFrame) and target column (pd.Series) if training.
               Processed features only if inference.

    Raises:
        RuntimeError: If preprocessing fails.
    """
    try:
        logging.info("Starting data preprocessing.")

        # Drop customerID
        if "customerID" in df.columns:
            df = df.drop(columns=["customerID"])
            logging.info("'customerID' column dropped.")

        # Handle missing values
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df.fillna({"TotalCharges": 0}, inplace=True)
        logging.info("Handled missing values in 'TotalCharges'.")

        # Separate target column for training
        target = None
        if True:#is_training
            target_column = "Churn"
            if target_column in df.columns:
                target = df[target_column].apply(lambda x: 1 if x == "Yes" else 0)
                df = df.drop(columns=[target_column])
                logging.info(f"Separated target column '{target_column}'.")

        # Encode categorical features
        categorical_columns = df.select_dtypes(include=["object"]).columns
        if not is_training:
            encoder = joblib.load("models/encoder.pkl")  # Load pre-trained encoder
        else:
            encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        encoded_categorical = pd.DataFrame(
            encoder.fit_transform(df[categorical_columns]),
            columns=encoder.get_feature_names_out(categorical_columns),
        )
        logging.info("Categorical features encoded.")

        # Scale numerical features
        numerical_columns = df.select_dtypes(include=["number"]).columns
        if not is_training:
            scaler = joblib.load("models/scaler.pkl")  # Load pre-trained scaler
        else:
            scaler = StandardScaler()
        
        # store training stage encoder scaler for future inference to ensure consistent feature encoding and scaling.
        if is_training:
            joblib.dump(encoder, "models/encoder.pkl")
            joblib.dump(scaler, "models/scaler.pkl")
        
        scaled_numerical = pd.DataFrame(
            scaler.fit_transform(df[numerical_columns]),
            columns=numerical_columns,
        )
        logging.info("Numerical features scaled.")

        # Combine processed features
        processed_data = pd.concat([scaled_numerical, encoded_categorical], axis=1)
        
        
        # Ensure all expected features are present
        if not is_training:
            with open(Config.MODEL_FEATURES_PATH, 'r') as file:
                features_data = json.load(file)
            expected_features = features_data["feature_names"]
            print('expected_features: ',expected_features)
        if not is_training and expected_features:
            for col in expected_features:
                if col not in processed_data.columns:
                    processed_data[col] = 0  # Add missing columns with default value
            processed_data = processed_data[expected_features]  # Reorder columns
            
        logging.info("Data preprocessing completed successfully.")

        if is_training:
            return processed_data, target
        else:
            return processed_data

    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        raise RuntimeError(f"Error during preprocessing: {e}")
