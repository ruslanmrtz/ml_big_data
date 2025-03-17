import os

from fastapi import FastAPI, UploadFile
import pandas as pd
import geopandas as gpd
import joblib
from PIL import Image
import numpy as np
import rasterio
from pandas.io.xml import preprocess_data

from models import SegmentPhoto, TrainModel

app = FastAPI()


@app.get('/')
def route():
    return {'message': 'hello'}


# функция загрузки снимка ДЗЗ.
@app.post('/load_image')
async def load_image(file: UploadFile):

    if validate_cart(file):

        with open(f'photos/{file.filename}', 'wb') as photo:
            print(await file.read())
            photo.write(await file.read())

        return {'filename': file.filename, 'message': 'success', 'size': file.size}
    return {'error': 'OAPFM<POAEK<FOPAE'}


# функция обработки снимков (отбраковка «не карт»).
def validate_cart(file: UploadFile):
    data = file.filename.split('.')
    if data[1] not in ['jpeg', 'png', 'tiff']:
        return False

    return True




#  функция определения и визуализации породного состава леса.
@app.get('/get_forest_info')
def get_forest_info():
    etalons = pd.read_csv('etalons_with_cluster.csv')

    woods_percentage = (etalons.groupby(['Mr1'])['area'].sum() / etalons['area'].sum() * 100) \
        .sort_values(ascending=False).round(2) \
        .apply(lambda x: f'{x}%').reset_index().rename(columns={'Mr1': 'Сокращение', 'area': '% распространения'})

    wood_fool = {'С': 'Сосна обыкновенная', 'Б': 'Берёза повислая',
                 '000000': 'Не покрытые древесно-кустарниковой растительностью',
                 'ОС': 'Осина', 'Е': 'Ель европейская', 'Л': 'Лиственница сибирская'}

    woods_percentage['Расшифровка'] = woods_percentage['Сокращение'].apply(lambda x: wood_fool[x])
    etalons['Расшифровка'] = etalons['Mr1'].apply(lambda x: wood_fool[x])

    return woods_percentage[['Сокращение', 'Расшифровка', '% распространения']].to_dict()

# функция сегментации изображений - кластеризации ареалов леса по типам, возрасту, запасам древесины
@app.get('/segmentate_forest')
def segmentate_forest(data: SegmentPhoto):
    model = joblib.load(filename='clustering.pkl')
    preprocessor = joblib.load(filename='preprocessor.pkl')
    df = pd.DataFrame({'area': data.area, 'avg_age': data.age, 'avg_tur1h': data.tur1h,
                       'avg_leaves': data.leaves, 'avg_conifer': data.conifer, 'avg_without_trees': data.without_trees}, index=[0])
    preprocessor_data = preprocessor.transform(df)
    print(preprocessor_data)
    cluster = model.predict(pd.DataFrame(preprocessor_data, columns=df.columns))
    return {'cluster': int(cluster[0])}


# функция для классификации видов леса на снимке (по Ареалам) и визуализации результатов
@app.get('/classification')
def classification(photo_path: str):
    model = joblib.load('model.pkl')

    photo = Image.open(f'photos/{photo_path}').convert('L').resize((138, 125))
    arr = np.asarray(photo)
    data = arr / arr.max()
    data = data.flatten().reshape(1, -1)
    prediction = model.predict(data)[0]
    return {'prediction': int(prediction)}


# функция для определения и визуализации зон вырубки.
@app.get('/get_clearcuts')
def get_clearcuts():
    clearcuts = gpd.read_file('../forests-wgs84/wgs84-etalons-clearcuts.shp')
    clearcuts['area'] = clearcuts.geometry.to_crs('EPSG:3857').area
    return clearcuts[['код', 'area']].to_dict()


# функция для выявления аномалии или деградации лесов на основе оценки фитомассы верхнего полога древостоя по разносезонным снимкам ДЗЗ

#  функция для выявления депрессивных зон леса в летние периоды – пожароопасные участки.


#  функция дообучения моделей
@app.post('/train_model')
def train_model(data: TrainModel):
    if data.photo_path not in os.listdir('photos'):
        return {'error': 'no such image'}
    if data.label not in [1, 2, 3]:
        return {'error': 'no such label'}

    model = joblib.load('model.pkl')

    photo = Image.open(f'photos/{data.photo_path}').convert('L').resize((138, 125))
    arr = np.asarray(photo)
    X = arr / arr.max()
    X = X.flatten().reshape(1, -1)
    model.fit(X, [data.label])
    joblib.dump(model, 'model.pkl')
    return {'result': 'success'}

