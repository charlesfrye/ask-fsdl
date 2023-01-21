# SETUP
from flask import Flask, request, jsonify

from dotenv import load_dotenv

load_dotenv()

import ask_fsdl

run_query = ask_fsdl.get_runner()


# CREATE FLASK APP AND ROUTES
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/prompt", methods=['POST'])
def prompt():
    content = request.get_json()
    text = content['text']
    response = run_query(text)  # execute
    return jsonify(response)
