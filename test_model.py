print("Testing imports...")
try:
    from facial_expression.prediction.predict import load_model_face
    print("✅ Imports successful!")
    
    print("Testing model load...")
    model = load_model_face()
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
