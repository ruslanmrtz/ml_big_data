import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib


def train_model_total_amount():
    con = sqlite3.connect('../data/taxi.db')

    sql = 'select * from taxi_for_regression'
    df = pd.read_sql(sql, con=con)

    X = df[['day', 'month', 'year', 'cluster']]
    total_amount = df['total_amount']

    # total_amount
    model_total_amount = LinearRegression()
    model_total_amount.fit(X, total_amount)

    joblib.dump(model_total_amount, 'model_total_amount.pkl')


def train_model_trip_distance():
    con = sqlite3.connect('../data/taxi.db')

    sql = 'select * from taxi_for_regression'
    df = pd.read_sql(sql, con=con)

    X = df[['day', 'month', 'year', 'cluster']]
    trip_distance = df['trip_distance']

    # total_amount
    model_trip_distance = LinearRegression()
    model_trip_distance.fit(X, trip_distance)

    joblib.dump(model_trip_distance, 'model_trip_distance.pkl')

