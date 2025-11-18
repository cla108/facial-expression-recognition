import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from gen_ai.gen_ai import question_pipeline_func
import requests
from PIL import Image
from facial_expression.prediction.predict import predict_emotion
from streamlit_cropper import st_cropper


def set_state(i):
    st.session_state.stage = i

# Page configuration
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'start' not in st.session_state:
    st.session_state.start = 0

if st.session_state.get("start") == 1:
    img_file = st.sidebar.file_uploader(label='Upload an image', type=['png', 'jpg','jpeg'], key=st.session_state.get("key"), accept_multiple_files=False)
    if img_file and st.session_state.stage == 0:
        set_state(1)

# starting page
if st.session_state.stage == 0:
    st.markdown("# FACIAL EXPRESSION ANALYSIS")
    st.markdown("#### Emotion Recognition AI")
    for i in range(0, 2):
        st.text("")


    st.markdown("""Welcome to EmotionAI, your trusted partner in understanding facial expressions!
                Our innovative AI software allows you to effortlessly analyze emotions from facial images.
                Simply upload an image and use our easy cropping tool to focus on the face you want to analyze.
                Our advanced technology will then analyze the image to detect the emotional expression.
                After receiving your result, you can ask for recommendations of songs or movies with our chat EmotionAI""", unsafe_allow_html=True)

    col4, col5, col6 = st.columns([1, 5, 1])
    for i in range(0, 3):
        col6.text("")

    botton1, botton2, botton3 = st.columns([5.6, 2, 5])
    if st.session_state.get("start") == 0:
        if botton2.button('start'):
            st.session_state.start = 1
            st.rerun()
    # facial expression related image
    image_path = "facial_expression_recognition.jpg"
    st.image(image_path, caption='', use_container_width=True)

    col5.text("")
    col5.markdown("##### Upload an image to analyze facial expressions")


# cropping page
if st.session_state.stage == 1:  # cropping an image
    if img_file:
        st.markdown("##### Select the face in your image:")
        st.text("")

        t1, t2 = st.columns([6, 4])
        tn1, tn2, tn3 = st.columns([6, 2, 2])

        with tn1:
            img = Image.open(img_file)

            # For faces, we don't have automatic detection yet, but you could add it later
            # try:
            #     default_coords = detect_face_bounding_box(img)  # You could implement this later
            # except:
            default_coords = None

            # Show image cropper tool
            image = st_cropper(img, realtime_update=True, box_color='#FF8505',
                            aspect_ratio=None, default_coords=default_coords,
                            return_type='image',
                            should_resize_image=True)

        t2.text("")

        # Show preview of the cropped image selection
        t2.write("Preview")
        tn2.image(image.resize((image.width * 150 // image.height, 150)))

        st.session_state.image = image

        # "Analyze" button accepts the user selection and starts prediction
        if tn3.button('analyze'):
            set_state(2)
            st.rerun()

# prediction and Q&A page
if st.session_state.stage == 2:
    st.session_state.image.convert('RGB').save('temp_image.jpg')
    with open('temp_image.jpg', 'rb') as f:
        with st.spinner('Analyzing facial expression...'):
            # Use Docker service name instead of localhost
            response = requests.post("http://facialexpressionrecognition-web-1:8000/predict", files={'file': f}).json()

    st.markdown("# FACIAL EXPRESSION ANALYSIS")
    st.markdown("#### Emotion Recognition Results")

    st.text("")

    # Updated response keys for facial expressions
    emotion = response['emotion']
    confidence = response['confidence']

    confidence_percentage = np.round(confidence, 3) * 100

    # Display the prediction
    pred1, pred2, pred3 = st.columns([3, 1, 8])
    for i in range(0, 2):
        st.text("")

    pred3.markdown("### Detected Emotion")
    if emotion:
        image = st.session_state.image
        pred1.text("")
        pred1.image(image.resize((image.width * 150 // image.height, 150)))

        # Color code emotions for better visual feedback
        emotion_colors = {
            'happy': '✅',
            'neutral': '⚪',
            'sad': '🔵',
            'angry': '🔴',
            'fear': '🟣',
            'surprise': '🟡',
            'disgust': '🟤'
        }

        emoji = emotion_colors.get(emotion, '😊')
        pred3.warning(f"{emoji} {emotion.upper()}, confidence {confidence_percentage}%")

        if pred3.button('analyze another image'):
            set_state(0)
            if st.session_state.get("key") == 1:
                st.session_state.key = 0
            else:
                st.session_state.key = 1
            st.rerun()

        for i in range(0, 13):
            pred2.text("")

        # Recommendation section - NOW INSIDE THE if emotion BLOCK
        st.markdown(f"#### Can we give you any recommendations related to {emotion}?")

        # Create two buttons side by side
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🎵 Recommend Music"):
                try:
                    response = requests.get("http://localhost:8000/answer_question",
                      params={'prediction': emotion, 'question': "Recommend some music that match this emotion"})
                    st.markdown("#### Music Recommendations:")
                    st.success(response.json()['answer'])
                except Exception as e:
                    st.error(f"Error getting music recommendations: {e}")

        with col2:
            if st.button("🎬 Recommend Movies"):
                try:
                    response = requests.get("http://localhost:8000/answer_question",
                      params={'prediction': emotion, 'question': "Recommend some movies that match this emotion"})
                    st.markdown("#### Movie Recommendations:")
                    st.success(response.json()['answer'])
                except Exception as e:
                    st.error(f"Error getting movie recommendations: {e}")

    else:
        st.write("The model couldn't detect an emotion from this image.")
        st.warning("You cannot ask a question until an emotion is detected.")
        st.stop()

# Add space before the bottom text
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("This application is designed for educational purposes only, not as psychological advice. The AI detects emotions from images, while the AI assistant answers questions about emotional understanding. 😊", unsafe_allow_html=True)
