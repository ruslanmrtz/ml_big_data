import streamlit as st
import db

st.title('Аналитическая система')


with st.sidebar:
    login = st.text_input('Введите логин')
    password = st.text_input('Введите пароль', type="password")
    auth_button = st.button('Войти')
    if auth_button:
        if login != '111' or password != '111':
            st.error('Неверный логин или пароль!')
            with open('auth.txt', 'w') as file:
                file.write('False')
        else:
            st.success('Успешный вход')
            auth = True
            with open('auth.txt', 'w') as file:
                file.write('True')

with open('auth.txt', 'r') as file:
    line = file.readline()
    auth = True if 'True' in line else False

if auth:
    st.subheader('Среднее количество человек на поездку в день')
    mean_passengers = db.get_mean_passenger_count()
    st.line_chart(mean_passengers, x='date', y='mean_passengers')

    st.subheader('Cуммарная стоимость поездок районах в неделю')
    week = st.number_input(step=1, min_value =1, max_value =53, label='Введите неделю')
    week_amount = db.get_week_amount(week)
    st.dataframe(week_amount)

    st.subheader('Cреднее суммарное количество чаевых в день за месяц')
    mean_tip = db.get_mean_tip()
    st.line_chart(mean_tip, x='month_tip', y='mean_tip')

    st.subheader('Cуммарное количество пассажиров в день')
    sum_passengers = db.get_sum_passenger_count()
    st.line_chart(sum_passengers, x='date', y='sum_passengers')

    st.subheader('Процентное соотношение количества поездок по способам оплаты за неделю')
    week1 = st.number_input(step=1, min_value=1, max_value=53, label='Введите неделю', key='acae')
    week_amount = db.get_week_count_by_type(week1)
    st.dataframe(week_amount)
