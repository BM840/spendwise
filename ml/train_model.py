import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
REVIEW_THRESHOLD = 0.60

df = pd.read_csv("transactions_train.csv")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'upi|neft|dr|cr|imps|rtgs', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
df["clean"] = df["description"].apply(clean_text)

vectorizer = TfidfVectorizer(ngram_range=(1,2))
X = vectorizer.fit_transform(df["clean"])
y = df["category"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained & saved")
