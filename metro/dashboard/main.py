import streamlit as st
import sqlite3
import pandas as pd
import datetime


st.title('Аналитическая панель')

# Подключение к базе данных
con = sqlite3.connect('data/db.db')
sql_get_stations = 'select distinct station from metro'
stations = pd.read_sql(sql_get_stations, con)['station'].tolist()


# Tоп самых загруженных станций
st.subheader('Tоп самых загруженных станций')
top_sql = '''select station, sum(num_val) as sum_val
from metro
group by station
order by sum_val desc'''
top_df = pd.read_sql(top_sql, con)
st.dataframe(top_df)
st.divider()


station_1 = st.selectbox(
    "Выберите станцию",
    stations,
)


date = st.date_input("Выберите дату", value=datetime.date(2023, 6, 1), min_value=datetime.date(2023, 1, 1), max_value=datetime.date(2023, 8, 31))
st.divider()

# Загруженность станции в процентах относительно максимальной загруженности.
st.subheader('Загруженность станции в процентах относительно максимальной загруженности.')

sql_busy = f"""
select avg(num_val) / (select max(num_val) from metro) * 100
from metro 
where date='{date.strftime('%Y-%m-%d')}' and station='{station_1}'
"""

busy_df = pd.read_sql(sql_busy, con)
st.metric(value=float(busy_df.round(2).iloc[0]), label='Процентов')


# Реальная пропускная способность станции
st.divider()
st.subheader('Реальная пропускная способность станции.')
sql_real_val = f"""
select sum(num_val)
from metro
where date='{date.strftime('%Y-%m-%d')}' and station='{station_1}'
"""
busy_real_val = pd.read_sql(sql_real_val, con)
st.metric(value=float(busy_real_val.round().iloc[0]), label='Человек')


# Cреднее количество пассажиров на станциях в течение заданного интервала времени
st.divider()
st.subheader('Cреднее количество пассажиров на станциях.')
sql_avg_val = f"""
select station, avg(num_val)
from metro
where date='{date.strftime('%Y-%m-%d')}'
group by station
"""
df_avg_val = pd.read_sql(sql_avg_val, con)
st.dataframe(df_avg_val)


# Kоличество станций без инфраструктуры для маломобильных граждан
st.divider()
st.subheader('Kоличество станций без инфраструктуры для маломобильных граждан.')
sql_without = f"""
select count(distinct station)
from metro
where output_escalator_count=0 and input_escalator_count=0
"""
df_without = pd.read_sql(sql_without, con)
st.metric(label='Количество станций', value=int(df_without.iloc[0]))