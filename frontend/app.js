const API = "https://my-music-bot-production-ee78.up.railway.app";

let tracks = [];
let currentIndex = 0;
let isPlaying = false;

async function search() {
  const query = document.getElementById("search").value;

  const res = await fetch(`${API}/search`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({query})
  });

  tracks = await res.json();

  const results = document.getElementById("results");
  results.innerHTML = "";

  tracks.forEach((track, index) => {
    const div = document.createElement("div");
    div.className = "track";
    div.innerText = track.title;

    div.onclick = () => play(index);

    results.appendChild(div);
  });
}

function play(index) {
  currentIndex = index;

  const track = tracks[index];
  const audio = document.getElementById("audio");

  audio.src = `${API}/play/${track.id}`;
  audio.play();

  document.getElementById("now").innerText = "▶ " + track.title;
  isPlaying = true;
}

function toggle() {
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