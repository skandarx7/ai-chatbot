import os
import base64
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Tum ek madadgar AI assistant ho.
Sawal ka seedha aur sahi jawab do.
Agar image bheji gayi ho to usay dekh kar jawab do.
Jawab Roman English mein do."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "OPENROUTER_API_KEY set nahi hai."}), 500

    user_input = request.form.get("prompt", "")
    
    payload = {
        "model": "google/gemma-2-9b-it:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "provider": {
            "allow_fallbacks": True
        }
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        data = response.json()
        if response.status_code == 200:
            answer = data["choices"][0]["message"]["content"]
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": data}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
