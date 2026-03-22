# 🎧 Telegram Music Mini App

Mini App для Telegram, который позволяет искать и слушать музыку через YouTube.

## 🚀 Функции
- 🔍 Поиск треков
- 🎵 Список результатов
- ▶️ Воспроизведение
- ⏭ Переключение треков
- ❤️ Рекомендации

## 🛠 Технологии
- Backend: FastAPI + yt-dlp
- Frontend: HTML / JS / CSS
- Deployment: Railway + Vercel

## ▶️ Запуск локально

### Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend
Открыть frontend/index.html

## 📡 API

- POST /search
- GET /play/{video_id}
- GET /recommend