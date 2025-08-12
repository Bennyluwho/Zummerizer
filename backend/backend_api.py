import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from newspaper import Article
from dotenv import load_dotenv

load_dotenv()  # loads .env next to this file
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
# Dev: allow everything. (Tighten later.)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize")
def summarize():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "No URL provided."}), 400

    # 1) Extract article text
    try:
        art = Article(url)
        art.download()
        art.parse()
        text = (art.text or "").strip()
        if not text:
            return jsonify({"error": "Failed to extract article content."}), 400
    except Exception as e:
        return jsonify({"error": f"Extractor error: {e}"}), 500

    # 2) Summarize with OpenAI
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a concise article summarizer."},
                {"role": "user", "content": "Summarize in 4–6 short bullet points:\n\n" + text}
            ],
            temperature=0.2,
            max_tokens=350
        )
        summary = resp.choices[0].message.content
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": f"OpenAI error: {e}"}), 500

if __name__ == "__main__":
    # Runs with: python summarizer.py
    app.run(host="127.0.0.1", port=5000, debug=True)
