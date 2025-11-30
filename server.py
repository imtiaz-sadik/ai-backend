from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
API_KEY = os.environ.get("GEMINI_API_KEY")
app = Flask(__name__)
CORS(app)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_prompt = request.json.get("prompt", "")
        answer = ask_gemini(user_prompt)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"❌ ERROR: {str(e)}"})
@app.route("/", methods=["GET"])
def home():
    return {"message": "AI Tutor server is running"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        resp = requests.post(GEMINI_URL, headers=headers, json=payload)
        data = resp.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"❌ Error: {str(e)}"})
