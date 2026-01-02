import os
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from app.db import engine
from app.api import lakes
from .api.auth import create_access_token, get_current_user

# ===== Для хэширования паролей через argon2 =====
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ===== Настройки приложения =====
app = FastAPI(title="Lakes API", version="0.1.0", docs_url=None, redoc_url=None)

# ===== CORS =====
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== API Routers =====
app.include_router(lakes.router)

# ===== Настройки админа =====
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD")  # в env хранится хэш argon2

# ===== Middleware для защиты Swagger =====
@app.middleware("http")
async def swagger_auth_middleware(request: Request, call_next):
    if request.url.path in ["/docs", "/redoc"]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
        token = auth_header.split(" ")[1]
        try:
            payload = get_current_user(token)
        except:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        if payload.get("sub") != "admin":
            return JSONResponse(status_code=403, content={"detail": "Forbidden"})
    return await call_next(request)

# ===== Эндпоинт для получения токена админа =====
@app.post("/admin/token")
def get_admin_token(username: str = Body(...), password: str = Body(...)):
    # проверяем username и пароль через argon2
    if username != ADMIN_USERNAME or not pwd_context.verify(password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    token = create_access_token({"sub": "admin"}, expires_delta=timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}

# ===== Swagger UI =====
@app.get("/docs", include_in_schema=False)
def swagger_ui():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="Lakes API Docs")

# ===== Пример токена обычного пользователя =====
@app.post("/token")
def login_for_access_token():
    user_data = {"sub": "user1"}
    access_token = create_access_token(user_data)
    return {"access_token": access_token, "token_type": "bearer"}

# ===== Пример защищённого эндпоинта =====
@app.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {"message": f"Hello {current_user['sub']}, you are authorized!"}

# ===== Здоровье сервиса =====
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ===== Тест подключения к БД =====
@app.get("/db-test")
def db_test():
    with engine.connect():
        return {"status": "connected"}
