from flask import Flask, render_template, request, jsonify
from llm_provider import LLMProvider
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

# Load config
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()
bot = LLMProvider(config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        reply = bot.chat(user_message)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
