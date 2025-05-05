import os
import random
import streamlit as st
from dotenv import load_dotenv
import time

# Map emotions to playlist search keywords
EMOTION_PLAYLISTS = {
    "happy": "happy hits",
    "sad": "sad songs",
    "angry": "rock metal",
    "fear": "chill ambient",
    "surprise": "new music",
    "neutral": "lofi beats",
    "disgust": "focus music"
}

def setup_spotify():
    """Set up and return Spotify client if credentials are available"""
    try:
        from spotipy import Spotify
        from spotipy.oauth2 import SpotifyClientCredentials
        
        load_dotenv()
        
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        
        # Check if credentials are available
        if not client_id or not client_secret:
            st.warning("Spotify API credentials not found. Please check your .env file.")
            return None
        else:
            # Create auth manager without timeout parameter
            auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
            
            # Create Spotify client with retries for connection issues
            sp = Spotify(auth_manager=auth_manager)
            return sp
    except Exception as e:
        st.error(f"Error setting up Spotify: {e}")
        return None

def get_music_recommendations(emotion, sp=None):
    """Get music recommendations based on detected emotion"""
    try:
        if sp is None:
            # Provide fallback recommendations if Spotify is not available
            st.warning("Spotify client not initialized. Using fallback recommendations.")
            return get_fallback_recommendations(emotion)
            
        query = EMOTION_PLAYLISTS.get(emotion.lower(), "lofi chill")
        
        with st.spinner(f"Searching for '{query}' playlists..."):
            # Handle potential network issues with retries
            max_retries = 3
            retry_delay = 2
            
            for attempt in range(max_retries):
                try:
                    results = sp.search(q=query, type='playlist', limit=1)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        st.warning(f"Connection attempt {attempt+1} failed. Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        st.error("Could not connect to Spotify API. Using fallback recommendations.")
                        return get_fallback_recommendations(emotion)
            
            playlists = results['playlists']['items']

            if not playlists:
                st.warning("No playlists found for this emotion")
                return get_fallback_recommendations(emotion)

            playlist_id = playlists[0]['id']
            playlist_name = playlists[0]['name']
            
            st.info(f"Found playlist: {playlist_name}")
            
            # Get tracks with retry logic
            for attempt in range(max_retries):
                try:
                    tracks_data = sp.playlist_tracks(playlist_id)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        st.error("Could not retrieve tracks. Using fallback recommendations.")
                        return get_fallback_recommendations(emotion)
            
            if not tracks_data or not tracks_data['items']:
                st.warning("No tracks found in the playlist")
                return get_fallback_recommendations(emotion)

            # Collect songs with preview URLs
            songs = []
            songs_without_preview = []
            
            for item in tracks_data['items']:
                try:
                    track = item['track']
                    if not track:
                        continue
                        
                    # Basic song info
                    song_info = {
                        "title": track['name'],
                        "artist": track['artists'][0]['name'] if track['artists'] else "Unknown Artist",
                        "album": track['album']['name'] if 'album' in track else "Unknown Album",
                        "preview_url": track.get('preview_url'),
                        "image_url": track['album']['images'][0]['url'] if track['album']['images'] else None,
                        "spotify_url": track['external_urls']['spotify'] if 'external_urls' in track else None
                    }
                    
                    if track.get('preview_url'):
                        songs.append(song_info)
                    else:
                        songs_without_preview.append(song_info)
                        
                except (AttributeError, KeyError, IndexError) as e:
                    continue

            # If we found songs with previews, return up to 5 random ones
            if songs:
                return random.sample(songs, min(5, len(songs)))
            elif songs_without_preview:
                st.warning("Found tracks, but none have playable previews")
                return random.sample(songs_without_preview, min(5, len(songs_without_preview)))
            else:
                return get_fallback_recommendations(emotion)

    except Exception as e:
        st.error(f"Spotify API Error: {type(e).__name__}: {str(e)}")
        return get_fallback_recommendations(emotion)

def get_fallback_recommendations(emotion):
    """Provide fallback song recommendations when Spotify API is unavailable"""
    emotion_fallbacks = {
        "happy": [
            {
                "title": "Happy",
                "artist": "Pharrell Williams",
                "album": "G I R L",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/60nZcImufyMA1MKQZ2Bm3n"
            },
            {
                "title": "Can't Stop the Feeling!",
                "artist": "Justin Timberlake",
                "album": "Trolls (Original Motion Picture Soundtrack)",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/1WkMMavIMc4JZ8cfMmxHkI"
            },
            {
                "title": "Uptown Funk",
                "artist": "Mark Ronson ft. Bruno Mars",
                "album": "Uptown Special",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS"
            }
        ],
        "sad": [
            {
                "title": "Someone Like You",
                "artist": "Adele",
                "album": "21",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/1qzWqfW8wP6koiwP79AZP0"
            },
            {
                "title": "Fix You",
                "artist": "Coldplay",
                "album": "X&Y",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q"
            },
            {
                "title": "All I Want",
                "artist": "Kodaline",
                "album": "In A Perfect World",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/4Bu8Hd1BgU1jnQHxbm3nOK"
            }
        ],
        "angry": [
            {
                "title": "Break Stuff",
                "artist": "Limp Bizkit",
                "album": "Significant Other",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/5cZqsjVoDCYvMXg3jcqmDH"
            },
            {
                "title": "Killing In The Name",
                "artist": "Rage Against The Machine",
                "album": "Rage Against The Machine",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/59WN2psjkt1tyaxjspN8fp"
            },
            {
                "title": "Enter Sandman",
                "artist": "Metallica",
                "album": "Metallica",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/1hKdDCpiI9mqz1jVHRKG0E"
            }
        ],
        "fear": [
            {
                "title": "Weightless",
                "artist": "Marconi Union",
                "album": "Weightless",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/1ZqHjApl3pfzxX8YsZcZ2p"
            },
            {
                "title": "Intro",
                "artist": "The xx",
                "album": "xx",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/2bzltP08x9K2KzZIdvgIrM"
            },
            {
                "title": "Clair de Lune",
                "artist": "Claude Debussy",
                "album": "Classical Essentials",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/303gZ4RVjtWWcB7BFfEoSs"
            }
        ],
        "surprise": [
            {
                "title": "Can't Feel My Face",
                "artist": "The Weeknd",
                "album": "Beauty Behind the Madness",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/22VdIZQfgXJea34mQxlt81"
            },
            {
                "title": "Thunder",
                "artist": "Imagine Dragons",
                "album": "Evolve",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/57pwwqu1R7F3eEuULUKl7l"
            },
            {
                "title": "Wow.",
                "artist": "Post Malone",
                "album": "Hollywood's Bleeding",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/7hQJA50XrCWABAu5v6QZ4i"
            }
        ],
        "neutral": [
            {
                "title": "Lofi Study",
                "artist": "Chillhop Music",
                "album": "Chillhop Essentials",
                "preview_url": None,
                "image_url": None,
                "spotify_url": "https://open.spotify.com/track/0KzG9nZkJ5yYkp36Trs7QG"
            },
            {
                "title": "Rainfall",
                "artist": "Ambient Sounds",
                "album": "Nature Sounds",
                "preview_url": None,
                "image_url": None,
                "spotify_url": None
            },
            {
                "title": "A Moment of Calm",
                "artist": "Peaceful Meditation",
                "album": "Mindfulness",
                "preview_url": None,
                "image_url": None,
                "spotify_url": None
            }
        ],
        "disgust": [
            {
                "title": "Thinking Clearly",
                "artist": "Focus Music",
                "album": "Deep Focus",
                "preview_url": None,
                "image_url": None,
                "spotify_url": None
            },
            {
                "title": "Concentration",
                "artist": "Study Music Academy",
                "album": "Focus Sessions",
                "preview_url": None,
                "image_url": None,
                "spotify_url": None
            },
            {
                "title": "Deep Work",
                "artist": "Brain.fm",
                "album": "Productivity",
                "preview_url": None,
                "image_url": None,
                "spotify_url": None
            }
        ]
    }
    
    # Get the fallback songs for the specific emotion, or use neutral as default
    songs = emotion_fallbacks.get(emotion.lower(), emotion_fallbacks["neutral"])
    
    st.warning("Using offline song recommendations due to connectivity issues with Spotify API.")
    return songs

def display_song(song):
    """Helper function to display song information"""
    with st.container():
        st.markdown(f"### {song.get('title', 'Unknown Track')}")
        st.markdown(f"**Artist:** {song.get('artist', 'Unknown Artist')}")
        
        if song.get('image_url'):
            st.image(song['image_url'], width=150)
        
        if song.get('preview_url'):
            st.audio(song['preview_url'], format="audio/mp3")
        else:
            st.info("Preview not available")
        
        if song.get('spotify_url'):
            st.markdown(f"[Open in Spotify]({song['spotify_url']})")
        
        st.markdown("---")