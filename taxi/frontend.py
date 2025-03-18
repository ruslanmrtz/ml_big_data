import streamlit as st
import requests


st.title('Предсказание характеристик')
day = st.number_input(min_value=1, max_value=30, label='Укажите день')
month = st.number_input(min_value=1, max_value=12, label='Укажите месяц')
year = st.number_input(min_value=2018, max_value=2025, label='Укажите год')

cluster = st.radio(
    "Выберите кластер",
    [1, 2, 3],
)

button_predict = st.button('Предсказать')

if day and month and year and cluster and button_predict:
    url = 'http://127.0.0.1:8000/predict_total_amount'
    total_amount = requests.get(url=url,
                       params={'day': day,
                               'month': month,
                               'year': year,
                               'cluster': cluster}).json()['prediction']

    st.subheader('Стоимость поездки')
    st.metric(' ', total_amount)

    url = 'http://127.0.0.1:8000/predict_trip_distance'
    trip_distance = requests.get(url=url,
                                params={'day': day,
                                        'month': month,
                                        'year': year,
                                        'cluster': cluster}).json()['prediction']
    st.subheader('Длина маршрута')
    st.metric(' ', trip_distance)

