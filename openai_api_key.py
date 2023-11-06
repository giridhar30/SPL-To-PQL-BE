# to read API key from file for OpenAI

import constants


def load():
    api_file = open(constants.openai_api_key_file, 'r')
    api_key = api_file.read()
    api_file.close()
    return api_key
