# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df
import numpy as np

from pydantic import BaseModel, ValidationError


class IrisInput(BaseModel):
    """
    Class to define the structure for the Unemployment model input data
    """
    Sepal_Length: float
    Sepal_Width: float
    Petal_Length: float
    Petal_Width: float


def orchestrator_function(context: df.DurableOrchestrationContext):
    # Get the input into the orchestrator function
    json_input = context.get_input()
    logging.info(f"Orchestrator recieved: {json_input}")

    # Validate the input
    try:
        IrisInput(**json_input)
        logging.info("Input validated successfully")
    except ValidationError as e:
        logging.error(f"Message validation failed, {e}")
        return {"Error": f"Message validation failed, {e}"}

    # Preprocess data for the model
    try:
        # Convert the input dict to a numpy array compatible with the model
        model_input = np.array(list(json_input.values())).reshape(1,-1)
        logging.info(f"Model input: {model_input}")
    except Exception as e:
        logging.error(f"Failed preparing data for model, {e}")
        return {"Error": f"Failed preparing data for model, {e}"}

    # Definte a list of tasks to be completed
    tasks = []
    # Define the list of models
    models = ["Model1"]#, "Model2", "Model3"]

    # Iterate through the list of models and start tasks for each one
    for model in models:
        tasks.append(context.call_activity(model, json_input))
    # Get the results from the tasks
    results = yield context.task_all(tasks)
    logging.info(results)
    # # Create a dictionary to store results
    # overall_results = {}
    # # Iterate over the list of models/results and populate output dict
    # for i in range(0, len(models)):
    #     overall_results[models[i]] = results[i]

    # return [overall_results]
    return json_input

main = df.Orchestrator.create(orchestrator_function)