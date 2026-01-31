import joblib
import re

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'upi|neft|dr|cr|imps|rtgs', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def predict(desc):
    clean = clean_text(desc)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    prob = max(model.predict_proba(vec)[0])
    print(f"{desc} → {pred} ({prob:.2f})")

# Test examples
predict("UPI/DR/JIO/PAYBILL")
predict("ATM ANN CHRG")
predict("OFFICE RENT SEPTEMBER")
predict("GST PAYMENT")
predict("ZEPTO GROCERY")
