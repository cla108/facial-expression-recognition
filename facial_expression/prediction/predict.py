from transformers import ViTForImageClassification, ViTImageProcessor
import torch

# Model cache
model_face = None
processor_face = None
emotion_labels = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

def load_model_face():
    """Load the facial expression model"""
    global model_face, processor_face
    if model_face is None:
        model_name = "trpakov/vit-face-expression"
        model_face = ViTForImageClassification.from_pretrained(model_name)
        processor_face = ViTImageProcessor.from_pretrained(model_name)
    return model_face

def predict_emotion(image):
    """Predict emotion from image using the Hugging Face model"""
    global model_face, processor_face

    if model_face is None:
        load_model_face()

    # Preprocess and predict
    inputs = processor_face(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model_face(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][predicted_class].item()

    emotion = emotion_labels[predicted_class]

    return emotion, confidence
