import pandas as pd
import logging
from sklearn.preprocessing import LabelEncoder


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the dataset by encoding categorical variables and handling missing values.

    Args:
        data (pd.DataFrame): Raw dataset.

    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    try:
        logging.info("Starting data preprocessing...")

        # Fill missing values
        data.ffill(inplace=True)

        # Encode categorical columns
        label_encoders = {}
        for col in data.select_dtypes(include=['object']).columns:
            logging.info(f"Encoding column: {col}")
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            label_encoders[col] = le

        logging.info("Data preprocessing completed.")
        return data
    except Exception as e:
        logging.error(f"Error in preprocessing: {e}")
        raise
