import os
import base64
import requests
from flask import Flask, request, jsonify, render_template

API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
MODEL = "google/gemma-4-31b-it:free"  # Image support wala model hona chahiye
URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Tum ek madadgar AI assistant ho.
Sawal ka seedha aur sahi jawab do.
Agar image bheji gayi ho to usay dekh kar jawab do.
Jawab Roman English mein do."""

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "OPENROUTER_API_KEY Vercel par set nahi hai."}), 500
    question = request.form.get("question", "").strip()
    image = request.files.get("image")

    content = []
    if question:
        content.append({"type": "text", "text": question})
    if image and image.filename:
        image_bytes = image.read()
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{image.mimetype};base64,{b64}"},
        })

    if not content:
        return jsonify({"error": "Sawal likhein ya image bhejein."}), 400

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]

    response = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "messages": messages},
        timeout=90,
    )

    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    answer = response.json()["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
