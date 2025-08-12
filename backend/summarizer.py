# backend/summarizer.py
import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from newspaper import Article
from dotenv import load_dotenv

# --- Load API key (local .env -> env var -> Render Secret File) ---
load_dotenv()  # reads backend/.env during local dev

def _load_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        secret_path = Path("/etc/secrets/OPENAI_API_KEY")
        if secret_path.exists():
            key = secret_path.read_text().strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY not found (env or /etc/secrets/OPENAI_API_KEY).")
    return key

client = OpenAI(api_key=_load_openai_key())

# --- Flask app ---
app = Flask(__name__)
# Dev-friendly CORS; tighten to specific origins for prod if you want
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
        article = Article(url)
        article.download()
        article.parse()
        text = (article.text or "").strip()
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
                {
                    "role": "user",
                    "content": "Summarize the article in a short paragraph response. "
                               "Focus on key facts, outcomes, and numbers when present.\n\n" + text
                },
            ],
            temperature=0.2,
            max_tokens=350,
        )
        summary = resp.choices[0].message.content
        return jsonify({"summary": summary})
    except Exception as e:
        # Avoid leaking internals to the client; check Render logs for details
        print(f"[OpenAI ERROR] {e}", flush=True)
        return jsonify({"error": "OpenAI request failed."}), 500

if __name__ == "__main__":
    # Local: defaults to 5000; Render: uses the provided $PORT
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
