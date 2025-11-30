import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

app = Flask(__name__)
CORS(app)

# 1️⃣ Function MUST be defined first
def ask_gemini(prompt):
    headers = {"Content-Type": "application/json", "X-goog-api-key": API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# 2️⃣ Route uses the function
@app.route("/ask", methods=["POST"])
def ask():
    user_prompt = request.json.get("prompt", "")
    answer = ask_gemini(user_prompt)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
