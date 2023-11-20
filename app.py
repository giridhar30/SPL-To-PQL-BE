from flask import Flask, request
from flask_cors import CORS

import constants
import converter
import openai
import openai_api_key

app = Flask(__name__)
CORS(app)

# loading the API key to the env
openai.api_key = openai_api_key.load()


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

    # Prepare the data object using converter.py
    data = converter.prepare_data(spl_code, preset)

    # Call the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=data["messages"],
            temperature=0,
            max_tokens=4011,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Extract the PQL code from the response
        pql_code = response.choices[0].message['content']  # Adjust based on actual response structure
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
        return {'success': 'false', 'message': 'Invalid preset name or messages'}, 400

    constants.add_new_preset(name, messages)
    return {'success': 'true', 'message': 'New preset added successfully.'}


@app.route('/preset', methods=['GET'])
def get_preset_names():
    return list(constants.PRESETS.keys())

'''
@app.route('/reset_presets', methods=['POST'])
def reset_presets():
    try:
        constants.reset_presets_to_base(mode = "soft") 
        # "soft" OR "hard" - hard reset resets the json file and soft reset does not.
        return jsonify({'message': 'Presets have been reset to base values.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''

if __name__ == "__main__":
    app.run(port=5000, debug=True)
