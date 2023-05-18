# Multi-Model-Deployment
Durable Functions are an extension of Azure Functions that lets you write stateful functions in a serverless compute environment. They offer the potential to create robust and scalable solutions for deploying multiple models quickly and easily.

## Python virtual environment
All of the following commands should be run in a terminal on a machine with python installed, a python download can be found [here](https://www.python.org/downloads/).
1) Create the virtual environment:
```
$py -m venv venv
```
2) Activate the virtual enviornment:
```
.\.venv\Scripts\activate
```
3) Done. It is as easy as that!
Bonus step is to install of all the required python packages from the requirements.txt
- Install the requirements:
```
pip install -r requirements.txt
```

<a id="item-one-b"></a>
## MLFlow Connection
As part of the advanced function models will be registered to, and loaded directly from managed MLFlow in Databricks, the below instructions will outline how to connect from your local machine to MLFlow.

If you do not already managed MLFlow you can try it for free using the link [here](https://www.databricks.com/product/managed-mlflow).

1) Generate a token from Databricks by going to *User Settings* -> *Access tokens* -> *Generate new token*
2) Run the following command:
```
databricks configure --token
```
3) Enter the databricks host URL & Token when prompted
If you have an MLFlow instance that is not managed by Databricks then you can simply ignore steps 1-3 and instead replace uri with that of your remote tracking servers. Replace line 8 in *Scripts/register_models.py* and line 12 in *Advanced/__init__.py* with:
```
mlflow_uri = "<Remote URI>"
```

## Running the Functions Locally
In order to run the Functions locally simply simply run the following command.
```
func start
```