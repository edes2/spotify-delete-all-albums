import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Credentials
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
REDIRECT_URI = 'http://127.0.0.1:8000/callback'

# Auth scopes: 'user-library-read' and 'user-library-modify' are required
scope = 'user-library-read user-library-modify'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

# Get all saved albums
def get_saved_albums():
    albums = []
    results = sp.current_user_saved_albums(limit=50)
    albums.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    return [album['album']['id'] for album in albums]

# Delete albums in batches of 20 (Spotify limit)
def delete_albums(album_ids):
    for i in range(0, len(album_ids), 20):
        batch = album_ids[i:i + 20]
        sp.current_user_saved_albums_delete(batch)
        print(f"Deleted {len(batch)} albums")

# Main
if __name__ == "__main__":
    print("Fetching saved albums...")
    albums = get_saved_albums()
    print(f"Found {len(albums)} albums.")
    if albums:
        delete_albums(albums)
        print("All albums removed.")
    else:
        print("No albums to remove.")
