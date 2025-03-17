import streamlit as st
import requests


st.title('Графический интерфейс пользователя')

api_url = 'http://127.0.0.1:8000'


with st.sidebar:
    st.header('Регистрация')

    fio = st.text_input('ФИО')
    company = st.text_input('Компания')
    job = st.text_input('Должность')
    email = st.text_input('e-mail')
    button = st.button('Зарегистрироваться')

    auth_data = fio and company and job and email

    if button and not auth_data:
        st.error('Введите все данные!')

    elif auth_data and button:
        st.session_state['success'] = True
        st.success('Успешная регистрация!')


if 'success' in st.session_state and st.session_state.success:
    file = st.file_uploader(label='Загрузите фото')
    print(file)
    if file:
        requests.post(f'{api_url}/load_image', files={'file': (file.name, file.getvalue())})
    # Загрузка в апи


#      Для «исторической» серии снимков строит динамику изменения зон вырубки, отображает
# их на карте, а также выводит график динамики площадей вырубки.


#     На основе «исторической» серии снимков определяет аномалии или деградации лесов на
# основе оценки фитомассы верхнего полога древостоя по разносезонным снимкам ДЗЗ.
# Участки аномалий и деградации выделяются и отмечаются.


# Реализована функция дообучения моделей.


else:
    st.error('Доступ доступен только после регистрации.')