import streamlit as st
import numpy as np
from PIL import Image

# 1. PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="FeelTune",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="auto"
)

# Import our modules
from emotion_model.emotion_utils import load_emotion_model, detect_emotion, get_emotion_emoji
from recommender.recommender import setup_spotify, get_music_recommendations, display_song

def process_image(img_file_buffer, emotion_model, spotify_client):
    """Handle image processing and music recommendation"""
    with st.spinner("Analyzing your mood..."):
        # Load and process image
        img = Image.open(img_file_buffer)
        img_array = np.array(img)
        
        # Detect emotion
        emotion = detect_emotion(img_array, model=emotion_model)
        
        # Show detected emotion with styling
        emoji = get_emotion_emoji(emotion)
        
        st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h2 style='text-align: center; margin: 0;'>I see you're feeling {emotion.upper()} {emoji}</h2>
            </div>
        """, unsafe_allow_html=True)

    # Get music recommendations
    st.markdown("## 🎵 Here's some music that matches your mood:")
    
    with st.spinner("Finding the perfect tracks for you..."):
        songs = get_music_recommendations(emotion, sp=spotify_client)
    
    if not songs:
        st.warning("No songs found for your mood. Try taking another photo!")
    else:
        # Display recommendations in a grid-like layout
        if len(songs) >= 3:
            cols = st.columns(3)
        else:
            cols = st.columns(len(songs))
            
        for i, song in enumerate(songs):
            col_idx = i % len(cols)
            with cols[col_idx]:
                display_song(song)

def main():
    # App header with styling
    st.markdown("""
        <div style='text-align: center'>
            <h1>🎧 FeelTune</h1>
            <h3>Emotion-Based Music Recommender</h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("Snap a photo to detect your mood and get matching music recommendations!")

    # Network status check (this will help diagnose connectivity issues)
    with st.expander("Check Network Status"):
        if st.button("Test Connectivity"):
            import socket
            
            def check_connection(host, port=443):
                try:
                    socket.create_connection((host, port), timeout=3)
                    return True
                except OSError:
                    return False
                    
            st.write("Testing connectivity to key services...")
            
            # Check Spotify API
            spotify_connected = check_connection("api.spotify.com")
            if spotify_connected:
                st.success("✅ Connection to Spotify API (api.spotify.com) is working")
            else:
                st.error("❌ Cannot connect to Spotify API (api.spotify.com)")
                st.info("If you're behind a proxy or firewall, make sure api.spotify.com is accessible")
            
            # Check general internet connectivity
            internet_connected = check_connection("www.google.com")
            if internet_connected:
                st.success("✅ Internet connection is working")
            else:
                st.error("❌ No internet connection detected")

    # Load models and services
    with st.spinner("Setting up..."):
        emotion_model = load_emotion_model()
        spotify_client = setup_spotify()
        
        if emotion_model is None:
            st.error("❌ Failed to load emotion detection model")
            st.info("Please make sure the model files are in the emotion_model directory")
        
        if spotify_client is None:
            st.warning("⚠️ Running without Spotify API - will use local recommendations")
            st.info("Check your .env file and internet connection")

    # Camera input
    img_file_buffer = st.camera_input("Take a picture", key="camera")

    # Process the image if available
    if img_file_buffer is not None:
        if emotion_model is None:
            st.error("Cannot process image: Emotion detection model not loaded")
        else:
            process_image(img_file_buffer, emotion_model, spotify_client)

    # About section
    with st.expander("About FeelTune"):
        st.markdown("""
        **FeelTune** uses:
        - Computer vision to detect your facial expression
        - Emotion classification to determine your mood
        - Spotify's API to find music that matches your emotion
        
        The app connects your emotional state to music, helping you find the perfect soundtrack for your mood!
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888888; font-size: 12px;'>
        Made with ❤️ by FeelTune Team
    </div>
    """, unsafe_allow_html=True)

# Entry point for the application
if __name__ == "__main__":
    main()