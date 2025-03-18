import streamlit as st
import datetime
import requests
import json

st.title('Прогнозирование прибыли компании с клиента по его параметрам')

channel = st.selectbox(
    "Канал привлечения",
    ['MediaTornado', 'AdNonSense', 'organic', 'LeapBob', 'FaceBoom',
     'TipTop', 'OppleCreativeMedia', 'RocketSuperAds', 'WahooNetBanner',
     'lambdaMediaAds', 'YRabbit'],
    index=None,
    placeholder="Выберите канал...",
)

device = st.selectbox(
    "Устройство",
    ['Mac', 'PC', 'Android', 'iPhone'],
    index=None,
    placeholder="Выберите устройство...",
)

region = st.selectbox(
    "Страна",
    ['Россия', 'Турция', 'Китай', 'Тайланд'],
    index=None,
    placeholder="Выберите страну...",
)

date = st.date_input("Дата", datetime.date(2022, 7, 6))

button = st.button('Расчитать прибыль')

if button:
    prediction = requests.get(f'http://127.0.0.1:8000/predict/{channel}/{device}/{region}/{str(date)}')

    st.metric(label='Прогноз (в у.е.)', value=prediction.text[1:-1])
