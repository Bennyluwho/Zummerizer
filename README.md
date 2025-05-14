
# 📰 Zummerizer - AI Article Summarizer

Zummerizer is a full-stack web application that uses AI to generate concise summaries of online articles. Just paste a URL, and let the AI do the rest!

---

## 🚀 Project Features
- AI-powered article summarization using OpenAI GPT models.
- Frontend built with React (Vite/CRA).
- Backend API using FastAPI.
- Clean JSON API integration between frontend and backend.

---

## 📂 Project Structure
```
Zummerizer/
├── backend/          # FastAPI Backend
│   ├── summarizer.py
│   └── backend_api.py
├── frontend/         # React Frontend
│   ├── App.jsx
│   └── main.jsx
└── README.md
```

---

## ✅ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/zummerizer.git
cd zummerizer
```

---

## 🎨 Frontend Setup (React)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React app:
```bash
# For Vite
npm run dev

# For Create React App
npm start
```

4. Open in your browser:
```
http://localhost:3000  (or port shown in terminal)
```

---

## 🛠️ Backend Setup (FastAPI)

1. Navigate to the backend directory:
```bash
cd backend
```

2. (Optional but recommended) Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:
```bash
python backend_api.py
```

5. API will be available at:
```
http://localhost:8000/summarize
```

---

## 🔑 Environment Variables

Create a `.env` file in the backend directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 📌 API Endpoint

- **POST /summarize**
    - **Request Body:**  
    ```json
    { "url": "https://example.com/article" }
    ```
    - **Response:**  
    ```json
    { "summary": "Your summarized content here..." }
    ```

---

## 🏁 Deployment Notes
- For frontend deployment, consider using **Vercel**, **Netlify**, or **AWS Amplify**.
- For backend deployment, use **AWS Lambda + API Gateway** or deploy directly via **EC2** or **Render**.

---

## 📚 License
MIT License

---

*Happy Summarizing! 🧠✨*
