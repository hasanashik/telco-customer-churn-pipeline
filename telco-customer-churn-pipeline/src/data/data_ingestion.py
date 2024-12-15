import pandas as pd
import logging

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a Pandas DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        logging.info(f"Loading data from {file_path}...")
        data = pd.read_csv(file_path)
        logging.info("Data loading completed.")
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise
