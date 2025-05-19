from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from newspaper import Article

# Load API Key from Render Secret File
with open("/etc/secrets/OPENAI_API_KEY", "r") as file:
    api_key = file.read().strip()

if not api_key:
    raise ValueError("❌ OpenAI API key is missing from the secret file.")

# Initialize OpenAI Client (new SDK syntax)
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)  # Allow frontend CORS requests

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()
        content = article.text

        if not content.strip():
            return jsonify({"error": "Failed to extract article content."}), 400

        response = client.chat.completions.create(
            model="gpt-4o",  # You can change to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "user", "content": f"Summarize the following article in concise bullet points:\n\n{content}"}
            ],
            max_tokens=300
        )

        summary = response.choices[0].message.content
        return jsonify({"summary": summary})

    except Exception as e:
        print(f"❌ Error occurred: {e}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
