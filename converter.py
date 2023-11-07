# converter.py
from constants import PRESETS

def prepare_data(system, selected_presets):
    """
    Prepare the data object to be sent to the OpenAI API based on the user's background setup
    and the selected presets.

    :param system: The background provided by the user.
    :param selected_presets: A list of preset names selected by the user.
    :return: A dictionary object structured for the OpenAI API.
    """
    # Start with a user message containing the SPL code
    messages = [{"role": "system", "content": system}]

    # Add preset messages based on the selected presets
    for preset_name in selected_presets:
        preset_messages = PRESETS.get(preset_name, [])
        messages.extend(preset_messages)

    # Construct the data object for the API
    data = {
        "messages": messages
    }

    return data
