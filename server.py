from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

API_KEY = "AIzaSyAkvX2qyIbjmk-uppwMPkPdokGqk__Y9wg"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_prompt = request.json.get("prompt")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-8b-instant",
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(GROQ_URL, json=data, headers=headers)
    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    return jsonify({"answer": answer})


@app.route("/")
def home():
    return "Backend is running!"