import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

app = Flask(__name__)
CORS(app)

def ask_gemini(prompt):
    if not API_KEY:
        return "❌ ERROR: Gemini API key not set in environment variables"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        data = response.json()

        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "❌ No text returned")
        elif "error" in data:
            return f"❌ API Error: {data['error']}"
        else:
            return f"❌ Unexpected API response: {data}"

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    user_prompt = request.json.get("prompt", "").strip()
    if not user_prompt:
        return jsonify({"answer": "❌ ERROR: No prompt provided"})
    answer = ask_gemini(user_prompt)
    return jsonify({"answer": answer})

@app.route("/", methods=["GET"])
def home():
    return "🔥 AI Tutor Backend is running! Use POST /ask with JSON { 'prompt': 'your question' }"

if __name__ == "__main__":
    print("🔥 AI Server running at http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000)
