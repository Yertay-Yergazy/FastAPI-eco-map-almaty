from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from passlib.context import CryptContext
from datetime import timedelta
import os

from app.db import engine
from app.api.auth import get_current_user, get_current_admin_user, create_access_token
from app.api.water_models import router as water_router
from app.services.firebase_service import initialize_firebase
from app.models import User
from app.schemas.user_schemas import UserResponse

# Контекст для хеширования паролей админа
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager - выполняется при старте и остановке приложения.
    """
    # Startup: инициализируем Firebase
    print("🚀 Starting application...")
    initialize_firebase()
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="Eco Map Almaty API",
    version="0.2.0",
    docs_url="/docs",
    lifespan=lifespan
)

# ===== CORS =====
origins = ["http://localhost:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Admin credentials =====
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD")

# ===== Public Endpoints =====
@app.get("/health", tags=["System"])
def health_check():
    """Проверка здоровья API"""
    return {"status": "ok", "version": "0.2.0"}

@app.get("/db-test", tags=["System"])
def db_test():
    """Проверка подключения к БД"""
    with engine.connect():
        return {"status": "connected"}

# ===== Admin Endpoints (JWT) =====
@app.post("/admin/token", tags=["Auth"])
def get_admin_token(username: str = Body(...), password: str = Body(...)):
    """
    Получить JWT токен для админа.
    
    Используется для входа админа (не через Firebase).
    Админ имеет полный доступ ко всем функциям системы.
    """
    if username != ADMIN_USERNAME or not pwd_context.verify(password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    token = create_access_token({"sub": "admin"}, expires_delta=timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}

# ===== User Endpoints (Firebase) =====
@app.get("/auth/me", response_model=UserResponse, tags=["Auth"])
def get_my_info(current_user: User = Depends(get_current_user)):
    """
    Получить информацию о текущем пользователе (Firebase).
    Требует Firebase токен в заголовке Authorization.
    """
    return current_user

# ===== API Routers =====
app.include_router(water_router)
