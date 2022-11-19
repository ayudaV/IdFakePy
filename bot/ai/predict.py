import joblib
def predict(text):
    model = joblib.load(open("ai/predict.py", "rb"))
    return model.predict([text])[0]