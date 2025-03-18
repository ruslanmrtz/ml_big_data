from fastapi import FastAPI
import numpy as np
import joblib

app = FastAPI()


@app.get('/predict_total_amount')
def predict_total_amount(day: int, month: int, year: int, cluster: int):
    '''Предсказание стоимости поездки'''
    X_test = np.array([[day, month, year, cluster]])

    model = joblib.load('model_total_amount.pkl')
    prediction = model.predict(X_test)[0]

    return {'prediction': prediction}


@app.get('/predict_trip_distance')
def predict_trip_distance(day: int, month: int, year: int, cluster: int):
    '''Предсказание длины поездки'''
    X_test = np.array([[day, month, year, cluster]])

    model = joblib.load('model_trip_distance.pkl')
    prediction = model.predict(X_test)[0]

    return {'prediction': prediction}