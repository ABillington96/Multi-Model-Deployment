# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import mlflow
import os
import azure.functions as func
import numpy as np
from mlflow.tracking import MlflowClient

# Setup the MLFlow client
mlflow_uri = "databricks"
client = MlflowClient(tracking_uri=mlflow_uri)
mlflow.set_tracking_uri(mlflow_uri)

# Create variable to store the model
MODEL = None

def load_model():
    """
    Function to load the model from MLFlow and assign it to the global MODEL variable
    """
    global MODEL
    MODEL = mlflow.sklearn.load_model(model_uri="models:/sk-learn-Logistic Regression-reg-model/Production")
    logging.info("Successfully loaded model sk-learn-Random Forest-reg-model from MLFlow")


def main(modelInput: list[int]) -> int:
    logging.info(f"Model1 recieved: {modelInput}")

    # If there is no model loaded, load the model
    if MODEL == None:
        try:
            logging.info("Loading model")
            load_model()
        except Exception as e:
            logging.error(f"Failed to load model, {e}")
            return f"Failed to load model"

    # Query the model
    try:
        prediction = MODEL.predict(np.array(modelInput).reshape(1,-1))
        logging.info(f"Prediction: {prediction}")
    except Exception as e:
        logging.error(f"Failed to query model, {e}")
        return "Failed to query model"

    return int(prediction[0])
