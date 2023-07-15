import json  # Импорт библиотеки JSON
import re
from typing import Any
import nltk
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

config_file = open("my_big_bot_config.json", "r", encoding="utf-8")  # Открытие файла
BOT_CONFIG = json.load(config_file)  # Преобразование из JSON в структуру данных


def normalize(text: str) -> str:
    """
        Создаем функцию, которая выкинет знаки препинания и приведет текст к нижнему регистру
    :param text: Ненормализованый текст
    :return: Нормализованый текст
    """
    text = text.lower()  # "ПРиВЕт" => "привет"
    # Удалять из текста знаки препинания с помощью "Regular Expressions"
    punctuation = r"[^\w\s]"  # выражение позволяет удалить все знаки препинания
    # ^ - "все кроме"
    # \w - "буквы"
    # \s - "пробелы"

    # Старое выражение = \W = "все кроме букв"
    return re.sub(punctuation, "",
                  text)  # Заменяем все что попадает под шаблон punctuation на пустую строку "" в тексте text


def is_matching(text1: str, text2: str) -> float:
    """
        Функция для сравнения текста пользователя со всеми текстами соответствующего индента
    :param text1: Текст полученый от пользователя
    :param text2: Все варианты текстов из соответствующего индента
    :return: Коэффициент схожести
    """
    text1 = normalize(text1)
    text2 = normalize(text2)
    print(text1, text2)
    distance = nltk.edit_distance(text1, text2)  # Посчитаем расстояние между текстами (насколько они отличаются)
    average_length = (len(text1) + len(text2)) / 2  # Посчитаем среднюю длину текстов
    return distance / average_length < 0.2


def get_intent(text: str) -> Any:  # Понимать намерение по тексту
    """
        Функция для определения намерения
    :param text: Текс от пользователя
    :return: Название намерения
    """
    all_intents = BOT_CONFIG["intents"]
    for name, data in all_intents.items():  # Пройти по всем намерениям и положить название в name, и остальное в переменную data
        for example in data["examples"]:  # Пройти по всем примерам этого интента, и положить текст в переменную example
            if is_matching(text, example):  # Если текст совпадает с примером
                return name


def get_answer(intent: str) -> Any:
    """
        Получаем ответ для отправки пользователю
    :param intent: Название намерения
    :return: Ответ пользователю на его сообщение
    """
    responses = BOT_CONFIG["intents"][intent]["responses"]
    return random.choice(responses)


def model_bot(text) -> Any:
    """
        Функция-бот
    :param text (str): Текст полученый от пользователя
    :return (str): Ответ пользователю
    """
    # Пытаемся опеределить намерение
    intent = get_intent(text)

    if not intent:  # Если намерение не найдено
        test = vectorizer.transform([text])
        intent = model.predict(test)[0]  # По Х предсказать у, т.е. классифицировать

    if intent:  # Если намерение найдено - выдать ответ
        return get_answer(intent)

    # Заглушка
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)


# тексты
x = []
# классы
y = []

# Задача модели по "x" научиться находить "y"
for name, data in BOT_CONFIG["intents"].items():
    for example in data["examples"]:
        x.append(example)  # Собираем тексты в "x"
        y.append(name)  # Собираем классы в "y"

vectorizer = CountVectorizer()  # В скобках можно указать настройки
vectorizer.fit(x)  # Передаём набор текстов, чтобы векторайзер их проанализировал
x_vectorized = vectorizer.transform(x)  # Трансформируем тексты в вектора (наборы чисел)

model = RandomForestClassifier()  # Настройки
model.fit(x_vectorized, y)  # Модель научится по "x" определять "y"

Countvect_RandomFor = model.score(x_vectorized, y)
