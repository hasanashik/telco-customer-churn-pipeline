import kagglehub
import shutil

# Correct path using a raw string
destination_path = r'F:\MLOPS poridhi\Module 3_ Building Machine Learning Workflow and Project Setup\exam\tasks\Task 1 Model Training with a Modular Workflow\telco-customer-churn-pipeline\data\raw'

path = kagglehub.dataset_download(
    'blastchar/telco-customer-churn', force_download=True
)

# Copy dataset to the destination
shutil.copytree(path, destination_path, dirs_exist_ok=True)
