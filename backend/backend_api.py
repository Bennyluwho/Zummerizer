import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from openai import OpenAI
from newspaper import Article

# --- OpenAI client from env var ---
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None

app = FastAPI(title="Zummerizer API", version="1.0.0")

# --- CORS: wide open for dev; tighten later ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    url: HttpUrl

class SummarizeResponse(BaseModel):
    summary: str | None = None
    error: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    if client is None:
        return SummarizeResponse(error="OPENAI_API_KEY is not set")

    # 1) Extract article text
    try:
        article = Article(str(req.url))
        article.download()
        article.parse()
        text = (article.text or "").strip()
        if not text:
            return SummarizeResponse(error="Failed to extract article content")
    except Exception as e:
        return SummarizeResponse(error=f"Extractor error: {e}")

    # 2) Summarize with OpenAI
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a concise article summarizer."},
                {"role": "user", "content": "Summarize in 4–6 short bullet points:\n\n" + text},
            ],
            temperature=0.2,
            max_tokens=350,
        )
        summary = resp.choices[0].message.content
        return SummarizeResponse(summary=summary)
    except Exception as e:
        return SummarizeResponse(error=f"OpenAI error: {e}")
