# Spotify Playlist Generator

This project helps you create a playlist on Spotify and add tracks to it using the Spotify Web API. Follow the steps below to configure your Spotify API, set up your environment, and run the script.

*Titles added might not be 100% accurate.*

## Prerequisites

1. **Python 3.x**: Ensure you have Python 3.x installed on your system.
2. **Spotipy Library**: This script uses the `spotipy` library to interact with the Spotify API.

## Step 1: Set Up Spotify API
1. **Create a Spotify Developer Account**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Log in with your Spotify account or create a new one.

2. **Create a New App**:
   - Click "Create an App" and fill in the required details.
   - Note the `Client ID` and `Client Secret` provided after creating the app.

3. **Set Redirect URI**:
   - In your app settings, add a Redirect URI. This should be `http://localhost:8888/callback` for this script.

## Step 2: Install Dependencies
Create a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install spotipy
```

## Step 3: Create config.json
Create a file named config.json in the same directory as your script with the following content:

```json
{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "redirect_uri": "http://localhost:8888/callback",
    "username": "your_username",
    "song_titles": ["song_title_1", "song_title_2", "song_title_3"]
}
```

Replace "your_client_id", "your_client_secret", and "your_username" with your Spotify application's Client ID, Client Secret, and your Spotify username respectively. Add the titles of the songs you want to include in the "song_titles" array.

## Step 5: Run the Script
To create the playlist and add the tracks, run the script using the following command:
```bash
python generate.py
```

## Troubleshooting
1. **Invalid Redirect URI**: Verify the Redirect URI matches exactly between your Spotify app settings and the config.json.
2. **Quota Issues**: If you encounter quota issues, reduce the frequency of API calls or check your Spotify API quota limits.

## Notes
1. **Scopes**: Ensure you request the appropriate scopes. playlist-modify-public is used in this example; for private playlists, you may need playlist-modify-private.
2. **Token Management**: The script handles token caching and refreshing. Ensure you manage your tokens securely.