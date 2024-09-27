from flask import Flask, request
from flask_cors import CORS
from macro_replacer import replace_or_remove_macros

import constants
import converter
from openai import OpenAI
import openai_api_key

app = Flask(__name__)
CORS(app)

client = OpenAI()

# API routes to be defined here
@app.route('/', methods=['GET'])
def hello_world():
    return {"success": True, "message": "Hello World!"}, 200


@app.route('/convert', methods=['POST'])
def convert_spl_to_pql():
    # Extract SPL code and selected preset from the request
    spl_code = request.json.get('spl_code')
    preset = request.json.get('preset')

    if not spl_code or not preset:
        return {'error': 'Missing SPL code or preset'}, 400

    # Call the OpenAI API
    try:
        spl_code = replace_or_remove_macros(spl_code, "SQL.csv")
        # Prepare the data object using converter.py
        data = converter.prepare_data(spl_code, preset)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=data["messages"],
            temperature=0,
            max_tokens=4011,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Extract the PQL code from the response
        pql_code = response.choices[0].message.content  # Adjust based on actual response structure
        return {'pql_code': pql_code}
    except Exception as e:
        # Handle exceptions and provide feedback
        return {'error': str(e)}, 500


@app.route('/preset', methods=['POST'])
def add_preset():
    # This is a simple example. In a real application, you should validate the input.
    name = request.json.get('name')
    messages = request.json.get('messages')
    
    if not name or not messages:
        return {'success': False, 'message': 'Invalid preset name or messages'}, 400

    try:
        constants.add_new_preset(name, messages)
        return {'success': True, 'message': 'New preset added successfully.'}, 200
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500


@app.route('/preset', methods=['GET'])
def get_preset_names():
    return list(constants.PRESETS.keys()), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
