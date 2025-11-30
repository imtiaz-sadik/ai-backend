from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")  # secure way
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def ask_gemini(prompt):
    if not API_KEY:
        return "❌ ERROR: Gemini API key missing"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    payload = {"contents":[{"parts":[{"text":prompt}]}]}
    
    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        data = response.json()
        # Safely extract text
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# API endpoint
@app.route("/ask", methods=["POST"])
def ask():
    user_prompt = request.json.get("prompt", "")
    answer = ask_gemini(user_prompt)
    return jsonify({"answer": answer})

# Serve HTML frontend
@app.route("/", methods=["GET"])
def index():
    return send_file("index.html")

# Serve static folder (CSS/JS if needed)
@app.route("/static/<path:path>")
def send_static(path):
    return send_file(f"static/{path}")

if __name__ == "__main__":
    print("🔥 AI Server running...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
