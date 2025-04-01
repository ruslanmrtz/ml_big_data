import streamlit as st
import librosa
import io

st.title("Аудио анализатор")

# Запись аудио
recorded_audio = st.audio_input("Запишите голосовое сообщение")
if recorded_audio:
    with open("audio.wav", "wb") as file:
        file.write(recorded_audio.read())
    st.success("Аудио записано!")

# Загрузка файлов
uploaded_files = st.file_uploader("Загрузите аудио", type=["wav"], accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.size > 5_000_000:
            st.error(f"{uploaded_file.name}: Файл слишком большой (более 5MB)")
            continue

        # Читаем файл в память
        bytes_data = uploaded_file.read()
        audio_buffer = io.BytesIO(bytes_data)

        # Загружаем и анализируем
        try:
            y, sr = librosa.load(audio_buffer, sr=None)
            rms = librosa.feature.rms(y=y).mean()

            if rms < 0.02:
                st.success(f"{uploaded_file.name}: Файл загружен и качественный!")
            else:
                st.error(f"{uploaded_file.name}: Файл слишком шумный!")
        except Exception as e:
            st.error(f"Ошибка обработки файла {uploaded_file.name}: {e}")
