from flask import Flask, request
import openai
from flask_cors import CORS
import openai_api_key
import os

app = Flask(__name__)
CORS(app)

# loading the API key to the env
os.environ['OPENAI_API_KEY'] = openai_api_key.load()


# API routes to be defined here
@app.route('/', methods=['GET'])
def hello_world():
    return {"success": "true", "message": "Hello World!"}, 200


@app.route('/api/converter', methods=['POST'])
def convert():
    data = request.get_json()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=data["messages"],
        temperature=0,
        max_tokens=2732,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message["content"]


if __name__ == "__main__":
    app.run(port=5000)
