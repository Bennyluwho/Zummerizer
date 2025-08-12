# Zummerizer

A tiny web app that turns an article URL into a clean summary.  
Frontend is a React/Vite single-page app; backend is a Flask service that extracts article text and asks OpenAI to summarize it.

---

## ✨ Features
- Paste any article URL → get a concise summary.
- Toast notifications and loading states in the UI.
- `/health` endpoint for quick uptime checks.
- Works locally with a `.env`, and on Render with either an env var **or** a Secret File for the API key.

---

## 🧰 Tech Stack
- **Frontend:** React + Vite, react-toastify
- **Backend:** Python, Flask, Flask-CORS, newspaper3k, OpenAI SDK

---

## 📂 Repo Structure
```
/
├─ backend/
│  ├─ summarizer.py        # Flask API (health + summarize)
│  └─ requirements.txt     # Flask + newspaper3k + openai, etc.
└─ src/                    # React app (Vite)
   ├─ App.jsx
   └─ main.jsx
```

---

## 🚀 Getting Started (Local)

### Prereqs
- Node 18+ and npm
- Python 3.10+
- An OpenAI API key

### 1) Backend (Flask)
```bash
cd backend
python -m pip install -r requirements.txt
# put your key in backend/.env (not committed)
# OPENAI_API_KEY=sk-xxx
python summarizer.py
```
- API will listen on `http://127.0.0.1:5000`
- Endpoints:
  - `GET /health` → `{"status":"ok"}`
  - `POST /summarize` with JSON `{ "url": "<article-url>" }` → `{ "summary": "..." }`

**Example curl**
```bash
curl -s -X POST http://127.0.0.1:5000/summarize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/article"}'
```

### 2) Frontend (Vite)
Use an environment variable for the API base so you never edit code when switching between local and prod.

Create these files in the repo root:

`.env.development`
```
VITE_API_BASE=http://127.0.0.1:5000
```

`.env.production`
```
VITE_API_BASE=https://zummerizer.onrender.com
```

Then run:
```bash
npm install
npm run dev
```

In your code, request the API via:
```js
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000";
await fetch(`${API_BASE}/summarize`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ url }) });
```

---

## ☁️ Production Deployment

### Backend on Render
1) **Service type:** Web Service (Python) linked to this repo
2) **Build Command**
```
pip install -r backend/requirements.txt
```
3) **Start Command** (choose one)
- Simple (dev server; fine for a personal demo):
```
python backend/summarizer.py
```
- Production (recommended, requires `gunicorn` in requirements):
```
cd backend && gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:$PORT summarizer:app
```
4) **Secrets**
- Preferred: add an **Environment Variable** named `OPENAI_API_KEY`
- Or: add a **Secret File** named `OPENAI_API_KEY` (Render mounts it at `/etc/secrets/OPENAI_API_KEY`). `summarizer.py` checks env first, then the secret file.

5) **CORS**
- During testing the backend allows all origins; restrict to your GitHub Pages domain when you go public.

**Health check:** `https://zummerizer.onrender.com/health`

### Frontend on GitHub Pages
- Build:
```bash
npm run build
```
- Deploy `dist/` using your Pages workflow. Make sure `.env.production` sets `VITE_API_BASE=https://zummerizer.onrender.com`.

---

## 🧠 How It Works
1) Frontend collects a URL and calls `POST /summarize` with JSON `{ url }`.
2) Backend downloads/parses the article with `newspaper3k`.
3) Backend asks OpenAI (`gpt-4o`) to produce a concise summary and returns it to the client.

---

## 🛠 Troubleshooting
- **“Failed to connect to backend.”**  
  Ensure the API base is correct (local vs prod) and the backend is running.
- **CORS errors in the browser**  
  Adjust allowed origins in `summarizer.py` CORS config.
- **Empty article text**  
  Some sites block scraping; try another URL. You can add a fallback extractor later.
- **OpenAI errors**  
  Verify your key and account status; check Render logs.

---

## 📄 License
Personal project. Add a license if you plan to accept contributions.