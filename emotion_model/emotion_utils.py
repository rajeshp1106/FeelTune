import cv2
import numpy as np
import streamlit as st
from keras.models import model_from_json

def load_emotion_model():
    """Load and return the emotion detection model"""
    try:
        # Load FER model
        with open('emotion_model/fer.json', 'r') as f:
            model = model_from_json(f.read())
        
        model.load_weights('emotion_model/fer.h5')
        return model
    except Exception as e:
        st.error(f"Error loading emotion model: {e}")
        return None

def detect_emotion(img, model=None, draw_box=False):
    """Detect emotion from image"""
    try:
        emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        if model is None:
            return "neutral"  # Fallback if model not loaded
            
        # Convert to grayscale if image is RGB/BGR
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img
            
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        emotions = []

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi_gray, (48, 48)) / 255.0
            roi_reshaped = roi_resized.reshape(1, 48, 48, 1)

            prediction = model.predict(roi_reshaped, verbose=0)
            max_index = np.argmax(prediction[0])
            emotion = emotion_labels[max_index]
            confidence = float(np.max(prediction[0]))

            emotions.append((emotion, confidence))

            if draw_box:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                label = f'{emotion} ({confidence*100:.1f}%)'
                cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Return most confident emotion or "neutral" if no face found
        if emotions:
            return max(emotions, key=lambda x: x[1])[0]
        else:
            return "sad"
    except Exception as e:
        st.error(f"Error in emotion detection: {e}")
        return "sad"

def get_emotion_emoji(emotion):
    """Return emoji based on emotion"""
    emotion_emoji = {
        "happy": "😊",
        "sad": "😢",
        "angry": "😠",
        "fear": "😨",
        "surprise": "😮",
        "neutral": "😐",
        "disgust": "🤢"
    }
    
    return emotion_emoji.get(emotion.lower(), "🤔")