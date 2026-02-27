from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.db import Base
import enum


class UserRole(str, enum.Enum):
    """
    Роли пользователей в системе:
    - guest: анонимный пользователь (не сохраняется в БД, используется для логики)
    - user: зарегистрированный пользователь (комментарии, публикации)
    - manager: менеджер (CRUD водоёмов, модерация контента)
    - admin: администратор (управление ролями пользователей)
    """
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    
    # Firebase UID вместо пароля (Firebase управляет аутентификацией)
    firebase_uid = Column(String, unique=True, nullable=False, index=True)
    
    full_name = Column(String, nullable=True)
    
    # Роль пользователя (по умолчанию - обычный пользователь)
    # Используем String вместо Enum для простоты миграций
    role = Column(
        String,
        nullable=False,
        default=UserRole.USER.value,
        server_default=UserRole.USER.value
    )
    
    # Активность аккаунта
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Временные метки
    created_at = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=False), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
