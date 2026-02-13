from flask import Flask, render_template_string
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
static_path = os.path.join(project_root, 'static')

app = Flask(__name__, static_folder=static_path, static_url_path='/static')

import os

def get_tracks():
    tracks = []
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        for filename in sorted(os.listdir(static_dir)):
            if filename.lower().endswith(".mp3"):
                tracks.append({
                    "name": f"♡ {filename.replace('.mp3','').replace('_',' ')} ♡",
                    "file": f"/static/{filename}"  # Flask serves this automatically
                })
    else:
        print("STATIC DIR NOT FOUND:", static_dir)
    return tracks


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>For You ♡</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

body {
    margin: 0;
    min-height: 100vh;
    background: url('https://i.pinimg.com/1200x/ae/5f/4a/ae5f4ab5acd4c84fc24aa43b887bcea6.jpg') no-repeat center center fixed;
    background-size: cover;
    display: flex;
    justify-content: center;
    align-items: center;
}

.card {
    background: #fff;
    width: 95%;
    max-width: 900px;   /* was 650px */
    padding: 50px;      /* was 35px */
    border-radius: 26px;
    border: 4px solid #ffb6c1;
    box-shadow: 0 15px 30px rgba(255, 182, 193, 0.6);
    text-align: center;
}

/* HEART */
.heart {
    width: 90%;
    max-width: 510px;
    cursor: pointer;
    animation: bounce 1.8s infinite;
    image-rendering: pixelated;
}

@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* SECTIONS */
.section {
    display: none;
    animation: pop 0.4s ease forwards;
}

@keyframes pop {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}

h2, h3 {
    font-family: 'Press Start 2P', cursive;
    color: #ff69b4;
    font-size: 14px;
}

p {
    background: #fff0f7;
    border: 2px dashed #ffb6c1;
    padding: 14px;
    border-radius: 12px;
    font-size: 20px;
    color: #444;
}

/* BUTTONS */
button {
    font-family: 'Press Start 2P', cursive;
    font-size: 10px;
    background: #ffb6c1;
    color: white;
    border: none;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 6px;
    cursor: pointer;
    box-shadow: 0 4px #ff69b4;
}

button:active {
    transform: translateY(2px);
    box-shadow: 0 2px #ff69b4;
}

/* CD */
.cd {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, #000 6%, #ffb6c1 7%, #ffb6c1 22%, #fff0f7 23%);
    margin: 14px auto;
    position: relative;
    box-shadow: 0 0 18px rgba(255,182,193,0.7);
}

.cd.spinning {
    animation: spin 4s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.cd img {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border: 3px solid white;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    body { align-items: flex-start; padding: 20px 0; }
    .card { padding: 24px; border-radius: 18px; max-width: 720px; }
    .heart { animation: bounce 1.6s infinite; }
    .cd { width: 140px; height: 140px; }
    .cd img { width: 90px; height: 90px; }
    h2, h3 { font-size: 13px; }
    p { font-size: 16px; }
    .photos img { height: 80px; }
    .track-list { max-height: 160px; }
}

@media (max-width: 420px) {
    .card { padding: 18px; border-radius: 14px; }
    .heart { width: 95%; max-width: 360px; }
    .cd { width: 110px; height: 110px; }
    .cd img { width: 80px; height: 80px; }
    button { font-size: 12px; padding: 10px 12px; }
    .photos { grid-template-columns: repeat(2, 1fr); gap: 6px; }
    .photos img { height: 72px; }
    p { font-size: 15px; }
    .track-item { font-size: 13px; }
    .progress-container { height: 12px; }
    .track-list { max-height: 140px; }
    .card { width: calc(100% - 24px); }
}

/* PROGRESS BAR */
.progress-container {
    width: 100%;
    height: 8px;
    background: #ffe0ec;
    border-radius: 6px;
    margin: 12px 0;
    border: 2px solid #ffb6c1;
    cursor: pointer;
}

.progress-bar {
    height: 100%;
    width: 0%;
    background: #ff69b4;
    border-radius: 4px;
}

/* PHOTOS */
.photos {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
}

.photos img {
    width: 100%;
    height: 90px;
    border-radius: 10px;
    border: 2px solid #ffb6c1;
    object-fit: cover;
    cursor: pointer;
    transition: all 0.2s ease;
}

.photos img:hover {
    border-color: #ff1493;
    box-shadow: 0 4px 12px rgba(255, 105, 180, 0.4);
    transform: scale(1.05);
}

/* LIGHTBOX */
#lightbox {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 1000;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.3s ease;
}

#lightbox.active {
    display: flex;
}

#lightbox img {
    max-width: 90%;
    max-height: 90%;
    border-radius: 15px;
    border: 5px solid #ffb6c1;
    cursor: pointer;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* TRACK LIST */
.track-list {
    background: #fff0f7;
    border: 3px solid #ffb6c1;
    border-radius: 12px;
    padding: 12px;
    margin: 12px 0;
    max-height: 200px;
    overflow-y: auto;
}

.track-item {
    cursor: pointer;
    padding: 8px;
    margin: 4px 0;
    border-radius: 8px;
    background: white;
    border: 2px solid #ffe0ec;
    transition: all 0.2s ease;
    font-size: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.track-item:hover {
    background: #ffe0ec;
    border-color: #ff69b4;
    transform: translateX(4px);
}

.track-item.active {
    background: #ffb6c1;
    border-color: #ff1493;
    font-weight: bold;
    color: white;
    image-rendering: pixelated;
}
</style>
</head>

<body>
<div class="card">

<img id="heart" class="heart"
src="https://i.pinimg.com/736x/f1/5b/5b/f15b5b2a1e35af90edbe2421185d417c.jpg"
onclick="openLetter()">

<div id="letter" class="section">
    <h2>♡ Hey, you! Read this :) ♡</h2>
    <p>
        Happy Valentine’s, Gurang!!! ♡<br><br>
        I hope this isn't too much, I just really wanted to make something special(?) for you. I don't really have much to say, I ran out of words already huhuhu sorry. Anyway, just make sure to read the letters and listen to the playlist I made hshshshshshsh <br><br>
        P.s. I recommend listening to the playlist while reading, and if u want the spotify link just tell me :] <br><br>
        I love you — always ♡
    </p>
    <button onclick="showPlayer()">💿 Music</button>
    <button onclick="showPhotos()">🎀 Letters</button>
</div>

<div id="playerSection" class="section">
    <h3>🎀 Songs that remind me of you 🎀</h3>

    <div class="cd" id="cd">
        <img src="https://i.pinimg.com/736x/0a/c9/4d/0ac94d35d7bac71e82a871f87af90075.jpg">
    </div>

    <div id="trackName">♡ our song ♡</div>

    <div class="progress-container" onclick="seek(event)">
        <div class="progress-bar" id="progress"></div>
    </div>

    <button onclick="prev()">⏮</button>
    <button onclick="togglePlay()">▶ / ❚❚</button>
    <button onclick="next()">⏭</button>

    <audio id="audio"></audio>

    <div class="track-list" id="trackList"></div>

    <br>
    <button onclick="back()">← back</button>
</div>

<div id="photoSection" class="section">
    <h3>🎀 Letters for you 🎀</h3>
    <div class="photos" id="photoGrid"></div>
    <button onclick="back()">← back</button>
</div>

<div id="lightbox" onclick="closeLightbox()"></div>

</div>

<script>
const tracks = {{ tracks_json | safe }};  // Dynamically loaded from server

let current = 0;
const audio = document.getElementById("audio");
const progress = document.getElementById("progress");
const trackName = document.getElementById("trackName");
const cd = document.getElementById("cd");
const trackList = document.getElementById("trackList");

// Debug audio loading
audio.addEventListener("error", (e) => {
    console.error("Audio error:", e);
    console.error("Error code:", audio.error?.code);
    console.error("Error message:", audio.error?.message);
});

audio.addEventListener("loadstart", () => console.log("Audio loading started"));
audio.addEventListener("canplay", () => console.log("Audio can play"));
audio.addEventListener("playing", () => console.log("Audio playing"));

function loadTrack() {
    const desired = tracks[current].file;
    // Only change src if it's different to avoid resetting playback
    if (!audio.src || !audio.src.includes(desired)) {
        const wasPlaying = !audio.paused && !audio.ended;
        const oldTime = audio.currentTime || 0;
        audio.src = desired;
        // Restore time if same track previously loaded via absolute/relative mismatch
        audio.addEventListener('loadedmetadata', function _restore() {
            try { if (oldTime && audio.duration > oldTime) audio.currentTime = oldTime; } catch(e) {}
            audio.removeEventListener('loadedmetadata', _restore);
        });
        if (wasPlaying) audio.play();
    }
    trackName.textContent = tracks[current].name;
    updateTrackListUI();
}

function updateTrackListUI() {
    document.querySelectorAll(".track-item").forEach((item, index) => {
        if (index === current) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });
}

function playTrack(index) {
    current = index;
    loadTrack();
    audio.play();
    cd.classList.add("spinning");
}

function initTrackList() {
    trackList.innerHTML = "";
    tracks.forEach((track, index) => {
        const item = document.createElement("div");
        item.className = "track-item";
        if (index === current) item.classList.add("active");
        item.textContent = track.name;
        item.onclick = () => playTrack(index);
        trackList.appendChild(item);
    });
}

function initPhotoGrid() {
    const photoGrid = document.getElementById("photoGrid");
    photoGrid.innerHTML = "";
    const photoUrls = [
        "https://i.pinimg.com/736x/12/02/af/1202afd5817d642aa52ab88c0fd0127b.jpg",
        "https://i.pinimg.com/originals/f5/00/40/f500400d6a5fc82dcf60566ee76d3823.gif",
        "https://i.pinimg.com/736x/9d/f8/48/9df848348c34c618fd25fdf85fe2a1e0.jpg",

        "https://i.pinimg.com/originals/e5/5b/15/e55b15f7b5e336593f33a5c0bf1bd311.gif",
        "https://i.pinimg.com/736x/33/55/58/335558adf12c0a6983cb31a362fabd19.jpg",
        "https://i.pinimg.com/originals/20/3e/b2/203eb26a52809af63f07e40850c35a87.gif",

        "https://i.pinimg.com/736x/93/ce/58/93ce583d5a330095395c67509d394b9c.jpg",
        "https://i.pinimg.com/originals/1a/4b/ed/1a4bedd86dc3e6f4f99a5741928db92e.gif",
        "https://i.pinimg.com/736x/b5/9c/cf/b59ccffa8c7663216baa85cc72a869ec.jpg"      
    ];
    
    photoUrls.forEach(url => {
        const img = document.createElement("img");
        img.src = url;
        img.onclick = (e) => openLightbox(url, e);
        photoGrid.appendChild(img);
    });
}

function openLightbox(src, e) {
    e.stopPropagation();
    const lightbox = document.getElementById("lightbox");
    lightbox.innerHTML = `<img src="${src}">`;
    lightbox.classList.add("active");
}

function closeLightbox() {
    document.getElementById("lightbox").classList.remove("active");
}

function togglePlay() {
    if (audio.paused) {
        audio.play();
        cd.classList.add("spinning");
    } else {
        audio.pause();
        cd.classList.remove("spinning");
    }
}

audio.addEventListener("timeupdate", () => {
    progress.style.width = (audio.currentTime / audio.duration) * 100 + "%";
});

audio.addEventListener("ended", next);

function seek(e) {
    const width = e.currentTarget.clientWidth;
    audio.currentTime = (e.offsetX / width) * audio.duration;
}

function next() {
    current = (current + 1) % tracks.length;
    loadTrack();
    audio.play();
}

function prev() {
    current = (current - 1 + tracks.length) % tracks.length;
    loadTrack();
    audio.play();
}

function openLetter() {
    heart.style.display = "none";
    letter.style.display = "block";
}

function showPlayer() {
    letter.style.display = "none";
    playerSection.style.display = "block";
    initTrackList();
    // Avoid reloading the audio if it's already set to the current track
    const desired = tracks[current].file;
    if (!audio.src || !audio.src.includes(desired)) {
        loadTrack();
        // don't force play; respect current paused state
    } else {
        // update UI and spinning state without touching audio playback
        trackName.textContent = tracks[current].name;
        updateTrackListUI();
        if (!audio.paused) cd.classList.add('spinning');
        else cd.classList.remove('spinning');
    }
}

function showPhotos() {
    letter.style.display = "none";
    photoSection.style.display = "block";
    initPhotoGrid();
}

function back() {
    document.querySelectorAll(".section").forEach(s => s.style.display = "none");
    letter.style.display = "block";
    cd.classList.remove("spinning");
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    tracks = get_tracks()
    tracks_json = json.dumps(tracks)
    return render_template_string(HTML, tracks_json=tracks_json)

if __name__ == "__main__":
    app.run(debug=True)



