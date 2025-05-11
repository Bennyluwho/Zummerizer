# Navigate to Backend and Start API
Start-Process powershell -ArgumentList "cd 'C:\Users\benja\Desktop\projects\Zummerizer\backend'; .\venv\Scripts\Activate; uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Navigate to Frontend and Start React App
Start-Process powershell -ArgumentList "cd 'C:\Users\benja\Desktop\projects\Zummerizer'; npm run dev"
