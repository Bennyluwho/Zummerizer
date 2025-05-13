from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import extract_article_text, summarize_text
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL instead of "*" for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    url: str

@app.post("/summarize")
def summarize(request: SummarizeRequest):
    try:
        article_text = extract_article_text(request.url)
        summary = summarize_text(article_text)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("backend_api:app", host="0.0.0.0", port=8000, reload=True)
