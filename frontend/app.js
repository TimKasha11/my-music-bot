let tracks = [];
let currentIndex = 0;
let isPlaying = false;

async function search() {
  const query = document.getElementById("search").value;

  const res = await fetch("http://127.0.0.1:8000/search", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({query})
  });

  tracks = await res.json();
  renderTracks(tracks, "results");
}

async function loadRecommendations() {
  const res = await fetch("http://127.0.0.1:8000/recommend");
  const data = await res.json();
  renderTracks(data, "recommend");
}

function renderTracks(list, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  list.forEach((track, index) => {
    const div = document.createElement("div");
    div.className = "track";
    div.innerText = track.title;
    div.onclick = () => play(index, list);
    container.appendChild(div);
  });
}

async function play(index, list = tracks) {
  currentIndex = index;
  tracks = list;

  const track = tracks[index];

  const res = await fetch(`http://127.0.0.1:8000/play/${track.id}`);
  const data = await res.json();

  const audio = document.getElementById("audio");

  audio.src = data.audio_url;
  audio.play();

  document.getElementById("nowPlaying").innerText = track.title;
  isPlaying = true;
}

function togglePlay() {
  const audio = document.getElementById("audio");

  if (isPlaying) {
    audio.pause();
  } else {
    audio.play();
  }

  isPlaying = !isPlaying;
}

function next() {
  if (currentIndex < tracks.length - 1) {
    play(currentIndex + 1);
  }
}

function prev() {
  if (currentIndex > 0) {
    play(currentIndex - 1);
  }
}

document.getElementById("audio").addEventListener("ended", next);

// загрузка рекомендаций при старте
loadRecommendations();