import joblib
from sklearn.pipeline import Pipeline

model:Pipeline = joblib.load("idfake_ai/model.pkl")

def isFake(text : str):
    return model.predict([text])[0]
