from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()


@app.get('/get_cluster')
def get_cluster(line:str, station_start: str, station_end: str,
                hour: int, day: int, month: int, year: int):

    data = pd.DataFrame({'line': [line], 'trip': [f'{station_start}-{station_end}'],
                         'hour': [hour], 'num_val': [600], 'output_escalator_count': [4],
                         'output_doors_count': [2], 'output_turnstile_count': [2], 'input_turnstile_total_bandwidth': [2],
                         'input_turnstile_count': [3], 'input_doors_count': [1], 'entry_id': [1],
                         'year': [year], 'month': [month], 'day': [day]})
    encoder = joblib.load('encoder.pkl')
    preprocessor = joblib.load('preprocessor.pkl')

    data[['line', 'trip']] = data[['line', 'trip']].apply(encoder.fit_transform)
    data = pd.DataFrame(preprocessor.transform(data), columns=data.columns)
    model = joblib.load('lr.pkl')
    pred = model.predict(data)
    return {'prediction': int(pred[0])}


@app.get('/get_num_val')
def get_num_val(model_name: str, year: int, month: int, day: int, cluster: int):
    data = pd.DataFrame({'year': [year], 'month': [month], 'day': [day], 'cluster': [cluster]})
    preprocessor = joblib.load('preprocessor_reg.pkl')
    data = pd.DataFrame(preprocessor.transform(data), columns=data.columns)

    if model_name == 'lin_reg':
        model = joblib.load('linear_reg.pkl')
        return int(model.predict(data)[0])
    elif model_name == 'ridge':
        model = joblib.load('ridge.pkl')
        return int(model.predict(data)[0])
    elif model_name == 'lasso':
        model = joblib.load('lasso.pkl')
        return int(model.predict(data)[0])
    else:
        return 0

