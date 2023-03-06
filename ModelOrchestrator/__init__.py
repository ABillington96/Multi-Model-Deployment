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


def orchestrator_function(context: df.DurableOrchestrationContext):
    # Get the input into the orchestrator function
    json_input = context.get_input()
    logging.info(f"Orchestrator recieved: {json_input}")

    # Preprocess the json input into a list of feature values
    model_input = list(json_input.values())
    logging.info(f"Processed input: {model_input}")

    # Definte a list of tasks to be completed
    tasks = []
    # Define the list of models
    models = ["Model1", "Model2", "Model3"]

    # Iterate through the list of models and start tasks for each one
    for model in models:
        tasks.append(context.call_activity(model, model_input))
    # Get the results from the tasks
    results = yield context.task_all(tasks)

    # Create a dictionary to store results
    overall_results = {}
    # Iterate over the list of models/results and populate output dict
    for i in range(0, len(models)):
        overall_results[models[i]] = results[i]

    return [overall_results]

main = df.Orchestrator.create(orchestrator_function)