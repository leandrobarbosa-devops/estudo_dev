import os
import threading
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

templates = Jinja2Templates(directory="templates")

frontend_app = FastAPI(title="Aplicação Frontend")

@frontend_app.get("/")
def home(request: Request):
    try:
        response = requests.get(BACKEND_URL)
        backend_data = response.json()
    except Exception as e:
        backend_data = {"error": str(e)}
    return templates.TemplateResponse("index.html", {"request": request, "backend_response": backend_data})

frontend_health_app = FastAPI(title="Health Check Frontend")

@frontend_health_app.get("/v1/health")
def health_check():
    return {"status": "ok"}

def run_frontend():
    uvicorn.run(frontend_app, host="0.0.0.0", port=8000)

def run_frontend_health():
    uvicorn.run(frontend_health_app, host="0.0.0.0", port=3030)

if __name__ == "__main__":
    threading.Thread(target=run_frontend).start()
    threading.Thread(target=run_frontend_health).start()
