from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from datetime import timedelta
from fastapi.responses import JSONResponse
import os

from app.db import engine
from app.api import lakes
from app.api.auth import create_access_token, get_current_user

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

app = FastAPI(title="Lakes API", version="0.1.0", docs_url="/docs")

# CORS
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD")  # хэш argon2 из .env

# ===== Эндпоинт admin токена =====
@app.post("/admin/token")
def get_admin_token(username: str = Body(...), password: str = Body(...)):
    if username != ADMIN_USERNAME or not pwd_context.verify(password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    token = create_access_token({"sub": "admin"}, expires_delta=timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}

# ===== Публичные эндпоинты =====
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/db-test")
def db_test():
    with engine.connect():
        return {"status": "connected"}

# ===== Lakes эндпоинт (только admin с токеном) =====
@app.get("/lakes")
def get_lakes(current_user=Depends(get_current_user)):
    # проверяем права admin
    if current_user.get("sub") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return [{"id": 1, "name": "Балхаш", "region": "Казахстан"}]

# ===== Остальные эндпоинты, публичные =====
@app.get("/protected")
def protected_route():
    return {"message": "Это публичный эндпоинт, токен не нужен!"}
