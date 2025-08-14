import plistlib
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# --- CONFIG ---
XML_FILE = "Path/Library.xml"  # chemin vers ton export Apple Music
SPOTIFY_USERNAME = "USERNAME"
PLAYLIST_NAME = "Apple Music Import"
# ---------------

# Authentification Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-public",
    username=SPOTIFY_USERNAME,
    redirect_uri="http://127.0.0.1:8888/callback",
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET"
))

# Création playlist
playlist = sp.user_playlist_create(SPOTIFY_USERNAME, PLAYLIST_NAME)
playlist_id = playlist["id"]

# Lecture de l'XML
with open(XML_FILE, 'rb') as f:
    library = plistlib.load(f)

tracks = library['Tracks']
to_add = []

for track_id, track_info in tracks.items():
    song = track_info.get("Name")
    artist = track_info.get("Artist")
    if not song or not artist:
        continue

    query = f"{song} {artist}"
    results = sp.search(q=query, type="track", limit=1)

    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        to_add.append(track_uri)
        print(f"✔ {song} - {artist}")
    else:
        print(f"✘ Not found: {song} - {artist}")

# Ajout en batchs de 100 pour éviter la limite API
for i in range(0, len(to_add), 100):
    sp.playlist_add_items(playlist_id, to_add[i:i+100])
    time.sleep(0.2)  # petit délai pour éviter un blocage

print(f"✅ Import terminé : {len(to_add)} morceaux ajoutés dans '{PLAYLIST_NAME}'")
