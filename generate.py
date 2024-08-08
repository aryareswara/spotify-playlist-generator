import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Load configuration and song titles from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

client_id = config['client_id']
client_secret = config['client_secret']
redirect_uri = config['redirect_uri']
username = config['username']
song_titles = config['song_titles']

# Authenticate with Spotify
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope='playlist-modify-public playlist-read-private')

def get_spotify_client():
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        token_info = sp_oauth.get_access_token()
    if token_info:
        token = token_info['access_token']
        return spotipy.Spotify(auth=token)
    else:
        print("No valid token available. Please check your authentication setup.")
        return None

sp = get_spotify_client()

if sp:
    try:
        # Fetch the current user’s ID
        current_user = sp.current_user()
        user_id = current_user['id']

        # Playlist name and description
        playlist_name = 'Anime OPs Collection'
        playlist_description = 'A collection of anime opening themes.'

        # Create a new playlist for the current user
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
        playlist_id = playlist['id']

        # Search for each song and add it to the playlist
        track_ids = []
        for title in song_titles:
            try:
                results = sp.search(q=title, limit=1, type='track')
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    track_ids.append(track['id'])
                    print(f"Added: {track['name']} by {track['artists'][0]['name']}")
                else:
                    print(f"Track not found: {title}")
            except spotipy.SpotifyException as e:
                print(f"Error searching for track '{title}': {e}")
                continue

        if track_ids:
            sp.playlist_add_items(playlist_id, track_ids)
            print(f"Tracks added to playlist '{playlist_name}'.")

        # Remove duplicates from the playlist after confirming creation
        playlist_tracks = sp.playlist_tracks(playlist_id)
        existing_track_ids = [item['track']['id'] for item in playlist_tracks['items']]
        unique_track_ids = list(set(existing_track_ids))
        
        # Remove duplicates by comparing original track IDs to the unique ones
        if len(existing_track_ids) > len(unique_track_ids):
            for track_id in existing_track_ids:
                if existing_track_ids.count(track_id) > 1:
                    sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])
            print(f"Removed duplicates from playlist '{playlist_name}'.")

        print(f"Playlist '{playlist_name}' created successfully!")

    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
