# converter.py
from constants import PRESETS


def prepare_data(spl_code, preset):
    """
    Prepare the data object to be sent to the OpenAI API based on the user's background setup
    and the selected presets.

    :param spl_code: The background provided by the user.
    :param preset: A list of preset names selected by the user.
    :return: A dictionary object structured for the OpenAI API.
    """
    preset_messages = PRESETS.get(preset, [])
    messages = preset_messages.copy()
    messages.append({"role": "user", "content": "SPL: \n" + spl_code})

    # Construct the data object for the API
    data = {
        "messages": messages
    }

    return data
