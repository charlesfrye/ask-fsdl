# SETUP
from flask import Flask, request, jsonify, send_from_directory

from dotenv import load_dotenv

load_dotenv()

import ask_fsdl

run_query = ask_fsdl.get_runner()


# CREATE FLASK APP AND ROUTES
app = Flask(__name__, static_url_path='', static_folder="frontend/dist")

@app.route("/")
def serve():
   return send_from_directory(app.static_folder,'index.html')

@app.route("/hello")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/prompt", methods=['POST'])
def prompt():
    content = request.get_json()
    text = content['text']
    response = run_query(text)  # execute
    return jsonify(response)


@app.route("/courses", methods=["GET"])
def courses():
    course_list = [{"name": "Full Stack Deep Learning",
                    "id": 1, "instructors": ["Charles Frye"]}]
    return jsonify(course_list)
