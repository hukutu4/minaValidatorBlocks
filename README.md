# Python MinaExplorer Blocks Log Script

This Python script retrieves the latest blocks data for a specified validator address from [MinaExplorer](https://minaexplorer.com) and logs them to a file. The script uses the following modules:

- `requests`: to make HTTP requests to the MinaExplorer API
- `json`: to parse JSON data from the API response and log data to a file
- `os`: to read environment variables for the validator address and log file name
- `dotenv`: to load environment variables from a `.env` file

## Setup
Install python and pip

```sudo apt install python3 python3-pip```

Before running the script, ensure that you have installed the required modules by running `pip install -r requirements.txt`. 

Next, сopy `.env.sample` to `.env` and set the following environment variables in a `.env` file:

- `VALIDATOR_ADDRESS`: the validator address for which to retrieve the blocks data
- `LOG_FILE_NAME`: the name of the log file to which the data will be logged

## Running the script

To run the script, simply execute `python3 log_blocks.py` in the terminal. 

The script first reads the StateHash of the last record in the log file (if it exists) and retrieves the latest blocks data from MinaExplorer. It then iterates over each block in the data array and logs the specified fields to the log file.

If a StateHash match is found in the log file, the script stops logging new records, assuming that all records after the match have already been logged. If no StateHash match is found in the log file, the script logs all records from the response data.