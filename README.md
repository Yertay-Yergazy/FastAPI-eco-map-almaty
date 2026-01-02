# Eco Map Almaty 🗺️

**Проект:** API для работы с озёрами Алматы с безопасной Swagger-панелью и JWT авторизацией.

## 🚀 Технологии
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blueviolet)
![Docker](https://img.shields.io/badge/Docker-24-blue)

## 💡 Описание
API позволяет:
- Получать список озёр
- Импортировать озёра в базу
- Генерировать токен администратора
- Защищать Swagger UI и эндпоинты
- JWT авторизация пользователей

## ⚡ Быстрый старт
1. Клонируем репозиторий: `git clone https://github.com/Yertay-Yergazy/FastAPI-eco-map-almaty`
2. Создаём venv и активируем
3. `pip install -r requirements.txt`
4. Настроить `.env`
5. `uvicorn app.main:app --reload`

## 🔒 Безопасность
- JWT токены
- Argon2 хэш для пароля администратора
- Swagger UI защищён
