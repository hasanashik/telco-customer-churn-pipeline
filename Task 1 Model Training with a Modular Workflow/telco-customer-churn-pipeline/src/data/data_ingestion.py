import pandas as pd
import logging


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load raw data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
        logging.info(f"Loading data from {file_path}...")
        data = pd.read_csv(file_path)
        logging.info("Data loading completed.")
        return data
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise
