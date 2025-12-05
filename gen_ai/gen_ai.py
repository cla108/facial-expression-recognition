# gen_ai/gen_ai.py
import os
import sys
from openai import OpenAI

# Add path to import MusicRecommender
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from facial_expression.music_recommender import MusicRecommender

# Initialize clients
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
music_recommender = MusicRecommender('spotify_emotions_curated.csv')

def question_pipeline_func(prediction, question):
    """Handle both music recommendations and general questions"""

    # Music-related questions
    music_keywords = ['music', 'song', 'playlist', 'recommend', 'track', 'artist']
    if any(keyword in question.lower() for keyword in music_keywords):
        return music_recommender.get_formatted_recommendations(prediction, n=10)

    # Other questions - use OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an emotion expert. The user's facial expression shows {prediction} emotion."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm sorry, I couldn't process your question. Error: {str(e)}"
