import os
import threading
import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.getenv("POSTGRES_USER", "default_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "default_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "default_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

backend_app = FastAPI(title="API de Processamento de Dados")

@backend_app.get("/")
def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).fetchone()
        return {"conexão realizada com sucesso! db_response": result[0]}
    except Exception as e:
        return {"error": str(e)}

backend_health_app = FastAPI(title="Health Check Backend")

@backend_health_app.get("/v1/health")
def health_check():
    return {"status": "ok"}

def run_backend():
    uvicorn.run(backend_app, host="0.0.0.0", port=8080)

def run_backend_health():
    uvicorn.run(backend_health_app, host="0.0.0.0", port=3030)

if __name__ == "__main__":
    threading.Thread(target=run_backend).start()
    threading.Thread(target=run_backend_health).start()
