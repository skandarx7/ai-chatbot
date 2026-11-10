import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
SYSTEM_PROMPT = """Tum ek madadgar AI assistant ho.
Sawal ka seedha aur sahi jawab do.
Jawab Roman English mein do."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "GEMINI_API_KEY set nahi hai."}), 500

    user_input = request.form.get("prompt", "")

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [
            {
                "parts": [{"text": user_input}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        data = response.json()
        if response.status_code == 200:
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": data}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
