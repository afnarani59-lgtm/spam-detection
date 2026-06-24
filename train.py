import os
import zipfile
import urllib.request
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# Configuration
DATASET_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
ZIP_FILE = "sms_spam_collection.zip"
DATA_FILE = "SMSSpamCollection"
MODEL_FILE = "model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

def download_and_extract():
    """Downloads the SMS Spam Collection dataset zip and extracts it."""
    if not os.path.exists(DATA_FILE):
        print(f"Dataset '{DATA_FILE}' not found. Downloading from UCI Repository...")
        try:
            # Set User-Agent to avoid potential blocks on direct automated downloads
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(DATASET_URL, ZIP_FILE)
            print("Download completed. Extracting files...")
            with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
                zip_ref.extractall(".")
            print("Extraction completed successfully.")
            # Clean up the zip file
            if os.path.exists(ZIP_FILE):
                os.remove(ZIP_FILE)
        except Exception as e:
            print(f"Error downloading or extracting dataset: {e}")
            raise
    else:
        print(f"Dataset '{DATA_FILE}' already exists locally.")

def load_data():
    """Loads the extracted dataset into a pandas DataFrame."""
    print("Loading data...")
    try:
        # The dataset is tab-separated and has no header.
        # It may contain non-UTF-8 characters, so we handle it by trying utf-8 first, then latin-1.
        try:
            df = pd.read_csv(DATA_FILE, sep='\t', header=None, names=['label', 'message'], encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(DATA_FILE, sep='\t', header=None, names=['label', 'message'], encoding='latin-1')
        print(f"Loaded {len(df)} records.")
        print(df['label'].value_counts())
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        raise

def train_and_evaluate():
    # 1. Download and extract
    download_and_extract()

    # 2. Load dataset
    df = load_data()

    # 3. Split dataset (stratify to preserve label distribution)
    print("Splitting dataset into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], 
        df['label'], 
        test_size=0.2, 
        random_state=42, 
        stratify=df['label']
    )

    # 4. Vectorize text using TF-IDF
    print("Vectorizing text data...")
    # Use lowercase=True, remove English stop words, and use bi-grams for better context capture
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # 5. Train Multinomial Naive Bayes classifier
    print("Training Multinomial Naive Bayes classifier...")
    # Adjust alpha for Laplace smoothing (alpha=0.1 gives better recall while maintaining high precision)
    model = MultinomialNB(alpha=0.1)
    model.fit(X_train_vec, y_train)

    # 6. Evaluate model
    print("Evaluating model...")
    y_pred = model.predict(X_test_vec)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision_spam = precision_score(y_test, y_pred, pos_label='spam')
    recall_spam = recall_score(y_test, y_pred, pos_label='spam')
    f1_spam = f1_score(y_test, y_pred, pos_label='spam')
    
    print("\n================ Evaluation Results ================")
    print(f"Accuracy:        {accuracy * 100:.2f}% (Target: >= 95%)")
    print(f"Precision (Spam): {precision_spam * 100:.2f}% (Target: >= 97%)")
    print(f"Recall (Spam):    {recall_spam * 100:.2f}% (Target: >= 90%)")
    print(f"F1-Score (Spam):  {f1_spam * 100:.2f}%")
    print("====================================================\n")
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # 7. Save model and vectorizer
    print(f"Saving vectorizer to '{VECTORIZER_FILE}'...")
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print(f"Saving model to '{MODEL_FILE}'...")
    joblib.dump(model, MODEL_FILE)
    print("Training process completed successfully.")

if __name__ == "__main__":
    train_and_evaluate()
