from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI(title="Music API", version="1.0")

# ✅ CORS (чтобы работал frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🎵 Поиск треков
def search_tracks(query):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch10:{query}", download=False)

        results = []
        for entry in info['entries']:
            results.append({
                "title": entry.get("title"),
                "id": entry.get("id")
            })

        return results

# 🎧 Получение аудио ссылки
def get_audio(video_id):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            f"https://youtube.com/watch?v={video_id}",
            download=False
        )

        # ищем лучший m4a (лучше всего для браузера)
        for f in info.get('formats', []):
            if f.get('ext') == 'm4a' and f.get('acodec') != 'none':
                return f['url']

        return info.get('url')


# 📡 API: поиск
@app.post("/search")
def search(data: dict):
    query = data.get("query")

    if not query:
        return JSONResponse({"error": "No query"}, status_code=400)

    results = search_tracks(query)
    return JSONResponse(results)


# ▶️ API: получить аудио
@app.get("/play/{video_id}")
def play(video_id: str):
    try:
        audio_url = get_audio(video_id)

        return JSONResponse({
            "audio_url": audio_url
        })

    except Exception as e:
        return JSONResponse({
            "error": str(e)
        }, status_code=500)


# ❤️ API: рекомендации (простые)
@app.get("/recommend")
def recommend():
    # просто популярные запросы
    queries = [
        "top hits 2024",
        "lofi hip hop",
        "Eminem",
        "Drake",
        "chill music"
    ]

    results = []
    for q in queries:
        results.extend(search_tracks(q)[:2])

    return JSONResponse(results)