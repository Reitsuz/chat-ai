from flask import Flask, request, jsonify, send_from_directory
from ai.brain import get_reply, learn
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "frontend"),
    static_url_path=""
)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data.get("text")

    reply = get_reply(text)
    learn(text, reply)

    return jsonify({"reply": reply})