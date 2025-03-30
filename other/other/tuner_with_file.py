import librosa
import numpy as np

# Частоты стандартного строя гитары (EADGBE)
GUITAR_STRINGS = {
    "E6": 82.41,  # Ми (6-я струна)
    "A5": 110.00,  # Ля (5-я струна)
    "D4": 146.83,  # Ре (4-я струна)
    "G3": 196.00,  # Соль (3-я струна)
    "B2": 246.94,  # Си (2-я струна)
    "E1": 329.63  # Ми (1-я струна)
}

# Загружаем аудиофайл
audio, sr = librosa.load('E_mi.mp3', sr=None)  # sr=None сохраняет исходную частоту дискретизации


def get_frequency(audio, sr):
    """Определяет основную частоту сигнала с помощью STFT."""
    stft = np.abs(librosa.stft(audio, n_fft=4096, hop_length=1024))  # Вычисляем STFT
    magnitude = stft.mean(axis=1)  # Средняя амплитуда по временной оси

    freq_bins = librosa.fft_frequencies(sr=sr, n_fft=4096)  # Соответствующие частоты для STFT
    peak_index = np.argmax(magnitude)  # Индекс максимальной амплитуды

    return freq_bins[peak_index]  # Возвращаем частоту с максимальной амплитудой


def get_fret_from_frequency(string, frequency):
    """Определяет, на каком ладу зафиксирован звук"""

    # Частоты для лада (каждый лад увеличивает частоту на полутон)
    SEMITONE_RATIO = 2 ** (1 / 12)
    
    open_freq = GUITAR_STRINGS[string]
    # Пытаемся найти лад, на котором будет данная частота
    fret = 0
    while open_freq * SEMITONE_RATIO ** fret < frequency:
        fret += 1
    return fret if open_freq * SEMITONE_RATIO ** fret - frequency < 5 else None  # Точность до 5 Гц


def get_tune(audio, sr):
    """Определяет наиболее близкую гитарную струну и отклонение частоты."""
    freq = get_frequency(audio, sr)  # Определяем основную частоту

    # Ищем ближайшую струну по частоте
    closest_string = min(GUITAR_STRINGS, key=lambda x: abs(GUITAR_STRINGS[x] - freq))
    deviation = freq - GUITAR_STRINGS[closest_string]  # Разница с эталонной частотой

    return closest_string, deviation  # Возвращаем название струны и отклонение


# Выводим результат
string, deviation = get_tune(audio, sr)
print(f"Определенная струна: {string}, отклонение: {deviation:.2f} Гц")
