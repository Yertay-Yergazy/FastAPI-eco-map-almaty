from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ===== Схемы для создания и регистрации =====
class UserCreate(BaseModel):
    """Схема для регистрации нового пользователя"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Пароль должен быть не менее 8 символов")
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Схема для входа пользователя"""
    email: EmailStr
    password: str


# ===== Схемы для ответов API =====
class UserResponse(BaseModel):
    """Схема для возврата информации о пользователе (без пароля)"""
    id: int
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy моделями


class TokenResponse(BaseModel):
    """Схема для возврата JWT токена"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
