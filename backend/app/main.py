from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from datetime import timedelta
import os

from app.db import engine
from app.api.auth import create_access_token
from app.api.water_models import router as water_router

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

app = FastAPI(
    title="Eco Map Almaty API",
    version="0.1.0",
    docs_url="/docs"
)

# ===== CORS =====
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Admin creds =====
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD")

# ===== Admin token =====
@app.post("/admin/token", tags=["Auth"])
def get_admin_token(username: str = Body(...), password: str = Body(...)):
    if username != ADMIN_USERNAME or not pwd_context.verify(password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    token = create_access_token(
        {"sub": "admin"},
        expires_delta=timedelta(hours=1)
    )
    return {"access_token": token, "token_type": "bearer"}

# ===== Public =====
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

@app.get("/db-test", tags=["System"])
def db_test():
    with engine.connect():
        return {"status": "connected"}

# ===== API Routers =====
app.include_router(water_router)
