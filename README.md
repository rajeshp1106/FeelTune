# 🎵 FeelTune – Emotion-Based Music Recommender 🎧

**FeelTune** is a real-time emotion-based music recommendation system built using **Streamlit**. It captures your facial expressions through webcam, detects your emotional state using deep learning, and recommends music tracks via the **Spotify Web API** that best align with how you feel.

---

## 🧠 Features

- 🎥 Real-time facial emotion detection (via webcam)
- 😄 Emotion classification: Happy, Sad, Angry, Neutral, etc.
- 🎶 Music recommendations powered by Spotify API
- 🔄 Seamless user experience using Streamlit’s interactive UI
- 🎧 Embedded Spotify player support

---

## 🛠️ Tech Stack

| Component         | Technology                              |
|------------------|------------------------------------------|
| Web Framework     | Streamlit                               |
| Face Detection    | OpenCV + TensorFlow/Keras/MediaPipe      |
| Emotion Model     | Pre-trained CNN (FER2013 or custom)      |
| Music API         | Spotify Web API                         |
| Language          | Python                                   |

---

## 📸 How It Works

1. User opens the Streamlit web app.
2. Webcam captures real-time video stream.
3. Emotion detection model processes the frame and classifies the emotion.
4. Emotion is mapped to a Spotify music mood.
5. Spotify API returns a playlist matching the detected emotion.
6. Songs are displayed with links or embedded players.

---

## 🧪 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/feeltune.git
cd feeltune

python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
Set up Spotify Developer Credentials
Go to Spotify Developer Dashboard

Create an app → get Client ID and Client Secret

Create a .env file:
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8501

streamlit run app.py
feeltune/
├── app.py
├── model/
│   └── emotion_model.h5
├── utils/
│   ├── spotify_api.py
│   └── emotion_mapper.py
├── requirements.txt
├── .env
└── README.md
