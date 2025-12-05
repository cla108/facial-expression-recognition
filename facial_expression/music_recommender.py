# music_recommender.py
import pandas as pd
import random

class MusicRecommender:
    def __init__(self, csv_path='spotify_emotions_curated.csv'):
        self.df = pd.read_csv(csv_path)
        print(f"Loaded {len(self.df)} songs from {csv_path}")

    def get_recommendations(self, emotion, n=10):
        """Get song recommendations for a specific emotion"""
        # Filter songs by emotion
        emotion_songs = self.df[self.df['emotion'] == emotion]

        if len(emotion_songs) == 0:
            return []

        # If we have fewer songs than requested, return all
        if len(emotion_songs) <= n:
            return emotion_songs[['artist', 'song', 'genre']].to_dict('records')

        # Randomly sample n songs
        sample = emotion_songs.sample(n=n)
        return sample[['artist', 'song', 'genre']].to_dict('records')

    def get_formatted_recommendations(self, emotion, n=10):
        """Get formatted string of recommendations"""
        recommendations = self.get_recommendations(emotion, n)

        if not recommendations:
            return f"No songs found for emotion: {emotion}"

        result = f"🎵 **{emotion.upper()} MUSIC RECOMMENDATIONS** 🎵\n\n"
        for i, song in enumerate(recommendations, 1):
            result += f"{i}. **{song['song']}** - *{song['artist']}* ({song['genre']})\n"

        return result
