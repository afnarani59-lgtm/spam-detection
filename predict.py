import os
import joblib

MODEL_FILE = "model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

def load_artifacts():
    """Loads the trained model and vectorizer files."""
    if not os.path.exists(MODEL_FILE) or not os.path.exists(VECTORIZER_FILE):
        print(f"Error: Trained model or vectorizer files not found.")
        print(f"Please make sure to run 'train.py' first to generate '{MODEL_FILE}' and '{VECTORIZER_FILE}'.")
        return None, None
    
    print("Loading model and vectorizer...")
    try:
        model = joblib.load(MODEL_FILE)
        vectorizer = joblib.load(VECTORIZER_FILE)
        print("Model and vectorizer loaded successfully!")
        return model, vectorizer
    except Exception as e:
        print(f"Error loading model or vectorizer: {e}")
        return None, None

def main():
    model, vectorizer = load_artifacts()
    if model is None or vectorizer is None:
        return

    print("\n" + "=" * 50)
    print("      SMS Spam Detection Interactive Predictor")
    print("=" * 50)
    print("Type your message to classify. Enter 'exit' or 'quit' to stop.\n")

    while True:
        try:
            message = input("Enter a message to classify: ").strip()
            if not message:
                continue
            if message.lower() in ['exit', 'quit']:
                print("Exiting predictor. Goodbye!")
                break

            # Vectorize the input message
            message_vec = vectorizer.transform([message])

            # Predict label and probabilities
            prediction = model.predict(message_vec)[0]
            probabilities = model.predict_proba(message_vec)[0]
            
            # Find index of the predicted class to get confidence
            classes = model.classes_
            class_idx = list(classes).index(prediction)
            confidence = probabilities[class_idx]

            # Format the output beautifully
            label_display = prediction.upper()
            color_prefix = "\033[91m" if label_display == "SPAM" else "\033[92m"
            color_suffix = "\033[0m"

            print(f"Prediction: {color_prefix}{label_display}{color_suffix}")
            print(f"Confidence: {confidence * 100:.2f}%")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nExiting predictor. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred during prediction: {e}")

if __name__ == "__main__":
    main()
