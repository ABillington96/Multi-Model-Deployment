# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
 
import logging

import azure.functions as func
import azure.durable_functions as df


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)

    # Read the message body
    try:
        json_msg = req.get_json()
        logging.info(f"Json message recieved: {json_msg}")
    except ValueError:
        logging.error("No json message recieved.")
        return func.HttpResponse(body="No json message recieved.", 
                             headers={"Content-Type": "application/json"},
                             status_code=500
    )

    instance_id = await client.start_new(req.route_params["functionName"], client_input=json_msg)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    return client.create_check_status_response(req, instance_id)