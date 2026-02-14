from flask import Flask, render_template_string
import json

app = Flask(__name__)

def get_tracks():
    return [
        {
            "name": "Our Playlist ♡",
            "iframe": """
            <iframe data-testid="embed-iframe"
            style="border-radius:12px"
            src="https://open.spotify.com/embed/playlist/3YwfUFBBgHjX35rzY7ECjj?utm_source=generator"
            width="100%"
            height="352"
            frameBorder="0"
            allowfullscreen=""
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy"></iframe>
            """
        }
    ]


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
        I hope this isn't too much, I just really wanted to make something special(?) for you. I don't really have much to say, I ran out of words already huhuhu sorry. Anyway, just make sure to read the letters I wroteand listen to the playlist I made hshshshshshsh <br><br>
        P.s. I recommend listening to the playlist while reading, and if u want the spotify link just tell me :] <br><br>
        I love you — always ♡
    </p>
    <button onclick="showPlayer()">💿 Music</button>
    <button onclick="showPhotos()">🎀 Letters</button>
</div>

<div id="playerSection" class="section">
    <h3>🎀 Songs that remind me of you 🎀</h3>

    <div id="spotifyPlayer"></div>

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

function openLetter() {
    heart.style.display = "none";
    letter.style.display = "block";
}

function showPlayer() {
    letter.style.display = "none";
    playerSection.style.display = "block";

    const spotifyDiv = document.getElementById("spotifyPlayer");
    spotifyDiv.innerHTML = tracks[0].iframe;

}


function showPhotos() {
    letter.style.display = "none";
    photoSection.style.display = "block";
    initPhotoGrid();
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
