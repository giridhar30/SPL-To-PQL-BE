import json

# files needed for the application
openai_api_key_file = 'openai-api-key.txt'
dataset_file = 'SPL-to-PQL-DataSet.xlsx'
# File to store presets
PRESETS_FILE = 'presets.json'

# Base presets
BASE_PRESETS = {
    "basic_conversion": [
        {"role": "system", "content": "Convert SPL to PQL."},
        {"role": "user", "content": "Search for error logs."},
    ],
    "advanced_conversion": [
        {"role": "system", "content": "Convert advanced SPL to PQL."},
        {"role": "user", "content": "Aggregate error logs by type and count."},
    ],
    # Add more base presets as needed
}

# Try to load presets from the file, if it exists
try:
    with open(PRESETS_FILE, 'r') as file:
        PRESETS = json.load(file)
except FileNotFoundError:
    # If the file does not exist, initialize with base presets
    PRESETS = BASE_PRESETS.copy()

# Current presets, initially set to base presets
def reset_presets_to_base(mode):
    """
    Resets the PRESETS to their base values.
    """
    global PRESETS
    PRESETS = BASE_PRESETS.copy()
    if mode == "hard":
        save_presets()


def save_presets():
    """
    Saves the current presets to the JSON file.
    """
    with open(PRESETS_FILE, 'w') as file:
        json.dump(PRESETS, file, indent=4)


def add_new_preset(name, messages):
    """
    Adds a new preset and saves it to the file.

    :param name: The name of the new preset.
    :param messages: A list of message dictionaries for the new preset.
    """
    PRESETS[name] = messages
    save_presets()

