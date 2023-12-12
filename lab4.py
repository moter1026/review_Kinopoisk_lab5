import pandas as pd 
import os
import csv
import nltk
from iterator import Iterator
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt
import re

nltk.download('punkt') # Загружаем необходимые ресурсы (требуется только при первом использовании)
nltk.download('wordnet')

def newSortDataFrame(data: pd.DataFrame, length: int) -> pd.DataFrame:
    """сортирует dataFrame, оставляя только те текстовые данные, длина"""
    return data[data["Count words"] <= length]


def filterDataframeByLabel(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """
    Функция фильтрует DataFrame по заданной метке класса.
    """
    return df[df["Class"] == label]


def plot_word_histogram(df: pd.DataFrame, label: str) -> None:
    """
    Функция строит гистограмму для слов в текстах, относящихся к указанной метке класса.
    """
    # Фильтруем DataFrame по метке класса
    filtered_df = df[df['Class'] == label]

    # Объединяем все тексты в одну строку
    text = ' '.join(filtered_df['Text of file'].astype(str))

    # Токенизируем текст на слова
    words = word_tokenize(text)
    clean_words = [re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', word) for word in words]
    # clean_words.remove(' ')
    word_counts = Counter(clean_words)
    top_words = word_counts.most_common(50)

    
    # Лемматизируем слова
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word, count in top_words]

    # Строим гистограмму
    plt.figure(figsize=(10, 6))
    plt.hist(lemmatized_words, bins=50, color='blue', edgecolor='black')
    plt.title(f'Гистограмма слов для метки класса "{label}"')
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = {
        "Class": [],
        "Text of file": [],
        "Count words": []
    }
    
    goodIter = Iterator("good")
    badIter = Iterator("bad")
    try_encodings = ["cp1251", "utf-8", "utf-8-sig", "latin-1"]
    
    for i, val in enumerate(goodIter):
        if i <= 1000:
            nameFile = val;
            for encoding in try_encodings:
                try:
                    with open(nameFile, "r", encoding=encoding) as readFile:
                        text_of_review = readFile.read()
                        words = nltk.word_tokenize(text_of_review)
                        data["Class"].append("good");
                        data["Text of file"].append(text_of_review);
                        data["Count words"].append(len(words));
                    break  # Прерываем цикл, если декодирование успешно
                except UnicodeDecodeError:
                    continue  # Переходим к следующей кодировке, если декодирование не удалось
        else:
            break
        
    
    for i, val in enumerate(badIter):
        if i <= 1000:
            nameFile = val;
            for encoding in try_encodings:
                try:
                    with open(nameFile, "r", encoding=encoding) as readFile:
                        text_of_review = readFile.read()
                        words = nltk.word_tokenize(text_of_review)
                        data["Class"].append("bad");
                        data["Text of file"].append(text_of_review);
                        data["Count words"].append(len(words));
                    break  # Прерываем цикл, если декодирование успешно
                except UnicodeDecodeError:
                    continue  # Переходим к следующей кодировке, если декодирование не удалось
        else:
            break

    # Проверяем наличие невалидных значений
    dfData = pd.DataFrame(data);
    print(dfData)

    # Проверяем наличие невалидных значений
    invalid_values = dfData.isna().any()

    # Обработка невалидных значений (замена пустых строк)
    if(invalid_values["Class"] == True):
        dfData.replace('', 'Неизвестно', inplace=True)
    if(invalid_values["Text of file"] == True):
        dfData = dfData[dfData["Text of file"] != '']
    
    # Вычисляем статистическую информацию для числовых столбцов
    numeric_stats = dfData.describe()
    print(numeric_stats)
    
    #Выводим результат функций из пунктов 6 и 7
    print(newSortDataFrame(dfData, 600))
    print(filterDataframeByLabel(dfData, "good"))

    # Группируем DataFrame по метке класса и вычисляем максимальное, минимальное и среднее значение по количеству слов
    grouped_dfData = dfData.groupby("Class")["Count words"].agg(['max', 'min', 'mean']).reset_index()
    print(grouped_dfData)

    plot_word_histogram(dfData, "good")

