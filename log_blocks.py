import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# get the value of the environment variable
validator_address = os.getenv("VALIDATOR_ADDRESS")

# set the URL for getting data
url = f"https://minaexplorer.com/all-blocks/{validator_address}?canonical=False&draw=1&start=0&length=10"

# set the log file name
log_file_name = os.getenv("LOG_FILE_NAME")
directory_path = os.path.dirname(log_file_name)
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# set the list of fields to output to the log file
fields_to_output = ["DateTime", "Epoch", "Slot", "BlockchainLength", "Transactions", "Coinbase", "StateHash", "BuiltOn"]

# find the StateHash of the last record in the log file
try:
    with open(log_file_name, "r") as f:
        last_line = f.readlines()[-1]
        last_state_hash = json.loads(last_line)["StateHash"]
except (FileNotFoundError, IndexError):
    # set last_state_hash to None if the file is not found or empty
    last_state_hash = None

# get data from the URL and parse JSON
response = requests.get(url)
data = json.loads(response.text)
# reverse the order of elements in the array to have dates from old to new (URL returns them from new to old)
data['data'].reverse()

# iterate over each element in the data array
found_last_state_hash = False
for block in data['data']:
    # create a dictionary with the fields to output to the log file
    fields_dict = {k: v for k, v in block.items() if k in fields_to_output}
    # get the value of the StateHash field from the current element
    current_state_hash = block['StateHash']

    if found_last_state_hash:
        # add a new line to the log file
        with open(log_file_name, "a") as f:
            f.write(json.dumps(fields_dict) + "\n")
    elif last_state_hash is None or current_state_hash == last_state_hash:
        # start adding new lines to the log file if last_state_hash is not set (file is empty),
        # or if a StateHash match is found
        found_last_state_hash = True

# if no StateHash match is found in the log file, add all records from the response data to the log file
if not found_last_state_hash:
    with open(log_file_name, "a") as f:
        for block in data['data']:
            # create a dictionary with the fields to output to the log file
            fields_dict = {k: v for k, v in block.items() if k in fields_to_output}
            f.write(json.dumps(fields_dict) + "\n")
