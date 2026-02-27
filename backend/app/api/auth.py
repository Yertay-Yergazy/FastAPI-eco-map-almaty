"""
Гибридная авторизация: JWT для админа + Firebase для пользователей

Система авторизации:
- Админ: JWT токены (username/password) - полный доступ
- Менеджер/Пользователь: Firebase токены - ограниченный доступ
- Гость: без авторизации - только просмотр карты
"""
import os
from datetime import datetime, timedelta
from typing import Optional, Union
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User, UserRole
from app.services.firebase_service import verify_firebase_token, initialize_firebase

# Загружаем .env
load_dotenv()

# JWT настройки для админа
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Bearer Token схема
bearer_scheme = HTTPBearer()


# ============================================================
# JWT ФУНКЦИИ ДЛЯ АДМИНА
# ============================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Создаёт JWT токен для админа.
    
    Args:
        data: Данные для включения в токен (обычно {"sub": "admin"})
        expires_delta: Время жизни токена
        
    Returns:
        str: JWT токен
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str) -> dict:
    """
    Проверяет JWT токен админа.
    
    Args:
        token: JWT токен
        
    Returns:
        dict: Payload токена
        
    Raises:
        HTTPException: Если токен невалиден
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token"
        )


# ============================================================
# DEPENDENCIES ДЛЯ АВТОРИЗАЦИИ
# ============================================================

def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """
    Dependency для админа (только JWT токены).
    
    Проверяет JWT токен и возвращает payload.
    Используется для админских endpoints.
    
    Returns:
        dict: {"sub": "admin", ...}
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    # Проверяем что это админ
    if payload.get("sub") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Универсальная dependency: принимает И JWT (админ) И Firebase (пользователи).
    
    Процесс:
    1. Пробует декодировать как JWT (для админа)
    2. Если не JWT — проверяет через Firebase
    3. Ищет/создаёт пользователя в БД
    """
    token = credentials.credentials
    
    # Шаг 1: Пробуем как JWT токен (для админа)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") == "admin":
            # Это JWT токен админа — ищем/создаём админа в БД
            admin_user = db.query(User).filter(User.email == "admin@eco-map.kz").first()
            if not admin_user:
                admin_user = User(
                    firebase_uid="jwt-admin",
                    email="admin@eco-map.kz",
                    full_name="Administrator",
                    role=UserRole.ADMIN.value,
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                db.refresh(admin_user)
            return admin_user
    except JWTError:
        pass  # Не JWT — пробуем Firebase
    
    # Шаг 2: Проверяем как Firebase токен
    firebase_user = verify_firebase_token(token)
    
    # Ищем пользователя в БД
    user = db.query(User).filter(User.firebase_uid == firebase_user['uid']).first()
    
    # Если пользователя нет - создаём (первый вход)
    if not user:
        user = User(
            firebase_uid=firebase_user['uid'],
            email=firebase_user['email'],
            full_name=firebase_user.get('name'),
            role=UserRole.USER.value,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ New user created: {user.email} (ID: {user.id})")
    
    # Проверяем активность аккаунта
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    return user


# ============================================================
# ROLE-BASED DEPENDENCIES
# ============================================================

def require_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency: Требует авторизованного пользователя Firebase (любая роль).
    
    Используйте в endpoints для зарегистрированных пользователей.
    """
    return current_user


def require_manager(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency: Требует роль manager или admin.
    
    Используйте в endpoints для создания/редактирования водоёмов.
    """
    if current_user.role not in [UserRole.MANAGER.value, UserRole.ADMIN.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or Admin role required"
        )
    return current_user


def require_firebase_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency: Требует роль admin от Firebase пользователя.
    
    Используйте в endpoints для управления ролями Firebase пользователей.
    """
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return current_user

