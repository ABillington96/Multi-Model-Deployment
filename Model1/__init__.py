# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import numpy as np


def main(modelInput: dict) -> int:
    logging.info(f"Model1 recieved: {modelInput}")
    return 0
