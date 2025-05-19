from newspaper import Article
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OpenAI API key is missing. Add it to your .env file.")

# Initialize OpenAI Client
client = OpenAI(api_key=api_key)

def extract_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following article:\n\n{text}"
            }
        ],
        max_tokens=300,
        temperature=0.5
    )
    return response.choices[0].message.content