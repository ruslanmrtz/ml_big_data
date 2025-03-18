from catboost import CatBoostRegressor
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import pickle

def preprocess_data(df):

    with open('encoder.pkl', 'rb') as file:
        encoder = pickle.load(file)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    cat_features = ['Channel', 'Device', 'Region']
    # Обработка категориальных признаков
    X_preprocess = encoder.transform(df[cat_features])
    X = pd.DataFrame(X_preprocess.toarray(), columns=encoder.get_feature_names_out())
    # добавляем дату
    X['day'] = df['date'].dt.day
    X['month'] = df['date'].dt.month
    X['day'] = df['date'].dt.year

    return X


def get_predict(channel, device, region, date):
    model = CatBoostRegressor()  # parameters not required.
    model.load_model('model.cbm')

    regions = {'Турция': 'Turkey',
               'Россия': 'Russia',
               'Китай': 'China',
               'Тайланд': 'Thailand'}

    df = pd.DataFrame({'Channel': [channel], 'Device': [device], 'Region': [regions[region]], 'date': [date]})
    X = preprocess_data(df)
    pred = model.predict(X)

    return pred.round(3)