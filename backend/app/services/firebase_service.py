"""
Firebase сервис для работы с аутентификацией

Этот модуль инициализирует Firebase Admin SDK и предоставляет
функции для проверки токенов пользователей.
"""
import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status
from typing import Dict, Optional


# Глобальная переменная - инициализирован ли Firebase
_firebase_initialized = False


def initialize_firebase():
    """
    Инициализирует Firebase Admin SDK.
    
    Поддерживает два способа:
    1. Переменная FIREBASE_CREDENTIALS_JSON в .env (для деплоя)
    2. Файл firebase-credentials.json (для локальной разработки)
    """
    global _firebase_initialized
    
    if _firebase_initialized:
        return
    
    # Способ 1: JSON из переменной окружения (для деплоя)
    firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if firebase_json:
        try:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            _firebase_initialized = True
            print("✅ Firebase initialized from environment variable")
            return
        except json.JSONDecodeError:
            print("⚠️ FIREBASE_CREDENTIALS_JSON is not valid JSON, trying file...")
    
    # Способ 2: JSON файл (для локальной разработки)
    cred_path = os.getenv(
        "FIREBASE_CREDENTIALS_PATH",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "firebase-credentials.json"
        )
    )
    
    if not os.path.exists(cred_path):
        raise FileNotFoundError(
            f"Firebase credentials not found. Either set FIREBASE_CREDENTIALS_JSON "
            f"in .env or place firebase-credentials.json at {cred_path}"
        )
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    
    _firebase_initialized = True
    print("✅ Firebase initialized from credentials file")


def verify_firebase_token(token: str) -> Dict:
    """
    Проверяет Firebase ID токен и возвращает информацию о пользователе.
    
    Args:
        token: Firebase ID token от клиента
        
    Returns:
        Dict с информацией о пользователе:
        {
            'uid': 'firebase_user_id',
            'email': 'user@example.com',
            'email_verified': True/False,
            'name': 'User Name' (если есть)
        }
        
    Raises:
        HTTPException: Если токен невалиден или истёк
    """
    if not _firebase_initialized:
        initialize_firebase()
    
    try:
        # Проверяем токен через Firebase
        decoded_token = auth.verify_id_token(token)
        
        # Извлекаем нужную информацию
        return {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'email_verified': decoded_token.get('email_verified', False),
            'name': decoded_token.get('name'),
        }
        
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


def get_firebase_user_by_email(email: str) -> Optional[Dict]:
    """
    Получает информацию о пользователе Firebase по email.
    
    Args:
        email: Email пользователя
        
    Returns:
        Dict с информацией о пользователе или None если не найден
    """
    if not _firebase_initialized:
        initialize_firebase()
    
    try:
        user = auth.get_user_by_email(email)
        return {
            'uid': user.uid,
            'email': user.email,
            'email_verified': user.email_verified,
            'display_name': user.display_name,
        }
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        print(f"Error getting Firebase user: {e}")
        return None
