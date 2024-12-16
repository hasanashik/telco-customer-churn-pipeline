# Building Machine Learning Workflow and Project Setup

![Image of Grafana dashboard](screenshots/ML-Pipeline.png)

## In this project our objectives are:

- Develop a modular training pipeline with Dataset tracking, Experiment tracking along with logging & versioning
- Deploy application with FastAPI and Docker to serve the trained model.
- Implement monitoring for the deployed API using Prometheus and Grafana.

## Project structure

telco-customer-churn-pipeline/<br/>
│<br/>
├── data/<br/>
│ ├── raw/<br/>
│ │ └──get_data.py<br/>
│ ├── processed/<br/>
│ └── final/<br/>
│<br/>
├── logs/<br/>
├── models/<br/>
│ ├── random_forest.pkl<br/>
│ └── features.json<br/>
├── provisioning/<br/>
│ └── datasources<br/>
│ └── prometheus-datasource.yml<br/>
├── src/<br/>
│ ├── data/<br/>
│ │ ├── **init**.py<br/>
│ │ ├── data_ingestion.py<br/>
│ │ └── preprocessing.py<br/>
│ ├── models/<br/>
│ │ ├── **init**.py<br/>
│ │ ├── train.py<br/>
│ │ └── predict.py<br/>
│ ├── utils/<br/>
│ │ ├── **init**.py<br/>
│ │ ├── logger.py<br/>
│ │ └── config.py<br/>
│ └── **init**.py<br/>
├── main.py<br/>
├── requirements.txt<br/>
├── Dockerfile<br/>
├── app.py<br/>
├── docker-compose.yml<br/>
├── prometheus.yml<br/>
└── setup_structure.sh<br/>

## To run the project

### Step 0: Download the dataset (WA*Fn-UseC*-Telco-Customer-Churn.csv) from Kaggle

Adjust the destination_path according to your folder name and then run the script get_data.py located in /data/raw directory. It will download telco-customer-churn data from kagglehub.
![Image of raw data downloaded](screenshots/0-raw-data-downloaded.jpg)

### Step 1: Train model

Run main.py located in the root directory of the project. It will load the data from raw directory and do preprocessing and then build a model in .pkl format along with features.json file.
All logs will be stored in \logs\project.log file.
![Image of model train and acuracy calculate](screenshots/1-main-py-model-train-and-acuracy-calculate.jpg)

### Step 2: Deploy application with FastAPI and Docker to serve the trained model

Run docker-compose file located in the root directory using
docker-compose up --build
It will up Grafana, fastapi_model and Prometheus containers. The datasource is located in /provisioning/datasources/prometheus-datasource.yml
node_exporter is used for monitoring the host server performance.

![Image of app deployment in container](screenshots/2-app-deployment-in-container.jpg)
After deploy the app inside a container we have:

- **app endpoint**: server_ip:8000/predict
- **Grafana**: server_ip:3000
- **Prometheus**: http:// server_ip:9090
- **node_exporter**: http:// server_ip:9100
  We will send POST request to app endpoint from Postman app with body:

```json
[
  {
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 2,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Mailed check",
    "MonthlyCharges": 53.85,
    "TotalCharges": 108.15
  }
]
```

![Image of Postman-POST-request](screenshots/3-Postman-POST-request.jpg)

We can see that the model predicted for this particular customer churn will not happen (prediction=0).

In Grafana we need to create dashboard now...
![Image of Grafana dashboard](screenshots/4-Grafana.jpg)
