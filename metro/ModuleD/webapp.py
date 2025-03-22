import streamlit as st
import requests
import pandas as pd


data = pd.read_excel('data/Dataset_с_параметрами_пропускной_способности_станций.xls')

st.subheader('Приложение')
st.title('Мое Метро 🚇')

st.divider()
st.subheader('Удобство поездки по определённому маршруту.')

line = st.selectbox(
    "Линия",
    data['line_name'].unique(),
)

start_station = st.selectbox(
    "Начальная станция",
    data['station_name'].unique(),
)

end_station = st.selectbox(
    "Конечная станция",
    data['station_name'].unique(),
)

date = st.date_input("Дата")
hour = st.time_input('Время')

cluster_button = st.button('Оценить')

if cluster_button:
    response = requests.get('http://127.0.0.1:8000/get_cluster/', params={'line': line, 'station_start': start_station,
                                                    'station_end': start_station, 'hour': hour.hour,
                                                    'year': date.year, 'month': date.month, 'day': date.day})
    if response.json()['prediction'] == 0:
        st.warning('Поездка нежелательна')
    if response.json()['prediction'] == 1:
        st.error('От поездки следует отказаться')
    if response.json()['prediction'] == 2:
        st.success('Поездка оптимальна')


st.divider()
st.subheader('Прогнозирования динамики изменения характеристик загруженности станций.')

model_name = st.radio(
    "Выберите модель",
    ["Линейная регрессия", "Ridge", "Lasso"])

date_val = st.date_input("Дата", key='adad')

cluster = st.radio(
    "Выберите кластер",
    ["1", "2", "3"])

button_val = st.button('Расчитать')

if button_val:
    models = {
        'Линейная регрессия': 'lin_reg',
        'Ridge': 'ridge',
        'Lasso': 'lasso'
    }

    response = requests.get('http://127.0.0.1:8000/get_num_val/', params={'model_name': models[model_name],
                                                                          'cluster': cluster,
                                                                          'year': date.year, 'month': date.month,
                                                                          'day': date.day})

    st.metric('Человек', response.text)


with st.sidebar:
    st.header('Справка по командам')
    st.write('Оценка оптимальности поездки')
    st.code('http://127.0.0.1:8000/get_cluster')
    st.table(pd.DataFrame({'Параметр': ['line', 'station_start', 'station_end', 'hour', 'day', 'month', 'year'],
              'Тип данных': ['str', 'str', 'str', 'int', 'int', 'int', 'int']}))
    st.write('Расчет нагруженности в указанный день')
    st.code('http://127.0.0.1:8000/get_num_val')
    st.table(pd.DataFrame({'Параметр': ['model_name', 'day', 'month', 'year'],
                           'Тип данных': ['str', 'int', 'int', 'int']}))