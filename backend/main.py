from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json

app = FastAPI()

# CORS (очень важно)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔍 Поиск
@app.post("/search")
async def search(data: dict):
    query = data.get("query")

    result = subprocess.run(
        ["yt-dlp", f"ytsearch10:{query}", "--dump-json"],
        capture_output=True,
        text=True
    )

    videos = []

    for line in result.stdout.split("\n"):
        if line.strip():
            video = json.loads(line)
            videos.append({
                "id": video["id"],
                "title": video["title"]
            })

    return videos


# 🎵 Стрим аудио (ГЛАВНОЕ ИСПРАВЛЕНИЕ)
@app.get("/play/{video_id}")
def play(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"

    process = subprocess.Popen(
        [
            "yt-dlp",
            "-f", "bestaudio",
            "-o", "-",
            url
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    return StreamingResponse(process.stdout, media_type="audio/mpeg")