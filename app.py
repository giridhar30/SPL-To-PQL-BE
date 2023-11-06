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


if __name__ == "__main__":
    app.run(port=5000)
