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

def search_for_track(sp, query):
    try:
        results = sp.search(q=query, limit=5, type='track')
        if results['tracks']['items']:
            return [track for track in results['tracks']['items'] if not any(
                term in track['name'].lower() for term in ['cover', 'karaoke']
            )]
        else:
            print(f"Track not found for query: {query}")
            return []
    except spotipy.SpotifyException as e:
        print(f"Error searching for track '{query}': {e}")
        return []

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
        track_names = {}
        added_track_ids = set()

        for title in song_titles:
            # Search using the provided title
            tracks = search_for_track(sp, title)
            if tracks:
                for track in tracks:
                    track_id = track['id']
                    
                    # Check if track ID is already in the set of added IDs
                    if track_id not in added_track_ids:
                        track_ids.append(track_id)
                        track_names[track_id] = f"{track['name']} by {track['artists'][0]['name']}"
                        added_track_ids.add(track_id)
                        print(f"Added: {track_names[track_id]}")
                        break  # Stop after finding the first valid track
                else:
                    print(f"No valid tracks found for query: {title}")
            else:
                # Attempt a broader search if the initial search fails
                variations = [
                    f"{title}"  # Adjust based on known details about the song
                ]
                for variation in variations:
                    tracks = search_for_track(sp, variation)
                    if tracks:
                        for track in tracks:
                            track_id = track['id']
                            if track_id not in added_track_ids:
                                track_ids.append(track_id)
                                track_names[track_id] = f"{track['name']} by {track['artists'][0]['name']}"
                                added_track_ids.add(track_id)
                                print(f"Added: {track_names[track_id]} (Variation)")
                                break  # Stop after finding the first valid track
                        break  # Stop after finding the first valid variation

        if track_ids:
            sp.playlist_add_items(playlist_id, track_ids)
            print(f"Tracks added to playlist '{playlist_name}'.")

        print(f"Playlist '{playlist_name}' created successfully!")

    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
else:
    print("Failed to get Spotify client.")
