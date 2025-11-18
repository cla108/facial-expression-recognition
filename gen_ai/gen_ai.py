def question_pipeline_func(prediction, question):
    """Temporary function until OpenAI API is set up"""

    # Simple responses based on emotion
    emotion_responses = {
        "happy": "Great! Happiness is wonderful. For music, try upbeat pop or joyful classical. For movies, comedies or feel-good films work well!",
        "sad": "I'm sorry you're feeling sad. For music, try comforting ballads or uplifting songs. For movies, heartfelt dramas or inspiring stories might help.",
        "angry": "It's okay to feel angry. For music, try intense rock or calming instrumental. For movies, action films or comedies can help release tension.",
        "fear": "Fear is a natural emotion. For music, try soothing ambient or calming classical. For movies, light comedies or inspiring stories might help.",
        "surprise": "Surprise can be exciting! For music, try unexpected jazz or energetic electronic. For movies, thrillers or adventure films could be fun!",
        "disgust": "Disgust is a protective emotion. For music, try powerful metal or cleansing world music. For movies, documentaries or transformative stories might help.",
        "neutral": "A neutral mood is balanced. For music, try lo-fi or smooth jazz. For movies, thoughtful dramas or documentaries could be interesting."
    }

    # Return a simple response based on the emotion
    base_response = emotion_responses.get(prediction, f"For {prediction} emotion, try music and movies that match this mood!")

    # Add the question context
    if "music" in question.lower():
        return f"🎵 Music recommendation for {prediction}: {base_response.split('.')[0]}."
    elif "movie" in question.lower():
        return f"🎬 Movie recommendation for {prediction}: {base_response.split('.')[1] if '.' in base_response else base_response}."
    else:
        return f"Emotion detected: {prediction}. {base_response}"
