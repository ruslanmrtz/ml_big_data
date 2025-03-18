from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from service import get_predict

app = FastAPI()

class User(BaseModel):
    Channel: str
    Device: str
    Region: str
    Date: str

@app.get('/')
def root():
    """
    Корневой get-запрос
    """
    return "root"


@app.get('/predict/{channel}/{device}/{region}/{date}', response_model=str)
def get_prompt(channel: str, device: str,
                  region: str, date: str):
    """
    Получение предсказания модели
    """

    prediction = get_predict(channel, device, region, date)

    return str(prediction[0])