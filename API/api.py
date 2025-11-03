import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
import warnings
warnings.filterwarnings('ignore')

from gen_ai.gen_ai import question_pipeline_func
from facial_expression.prediction.predict import predict_emotion, load_model_face
from fastapi import FastAPI, File, UploadFile
from PIL import Image

app = FastAPI()

# Load the facial expression model
model_face = load_model_face()

@app.get('/answer_question')
def ask_questions(prediction, question):
    output = question_pipeline_func(prediction, question)
    return {'answer': output}

@app.post('/predict')
async def prediction(file: UploadFile):
    img = Image.open(file.file)
    emotion, confidence = predict_emotion(img)
    return {'emotion': emotion, 'confidence': float(confidence)}
