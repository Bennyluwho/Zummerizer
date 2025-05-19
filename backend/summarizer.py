from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
from newspaper import Article

# Load environment variables
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise ValueError("❌ OpenAI API key is missing. Add it to your .env file.")

with open("/etc/secrets/OPENAI_API_KEY", "r") as file:
    api_key = file.read().strip()

if not api_key:
    raise ValueError("❌ OpenAI API key is missing from the secret file.")

openai.api_key = api_key

app = Flask(__name__)
CORS(app)  # This allows all origins by default

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

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Summarize the following article:\n\n{content}"}],
            max_tokens=300
        )
        summary = response.choices[0].message.content
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
