import csv
from typing import Dict, List

import pandas as pd


def read_transactions_csv(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из CSV-файла.
    :param file_path: Путь к CSV-файлу.
    :return: Список словарей, каждый из которых представляет собой одну операцию.
    """
    opera = []  # Список для хранения операций
    with open(file_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)  # Создаем объект для чтения словарей
        for row in reader:
            opera.append(row)  # Добавляем каждую строку в список операций
    return opera


# Пример использования функции:
operations_1 = read_transactions_csv(r"C:\Users\User\pythonProject5.1(0)\data\transactions.csv")
print(operations_1)


def read_transactions_xlsx(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из XLSX-файла.
    :param file_path: Путь к XLSX-файлу.
    :return: Список словарей, каждый из которых представляет собой одну операцию.
    """
    opera_1 = pd.read_excel(file_path)  # Читаем файл Excel с помощью Pandas
    return opera_1.to_dict("records")  # Преобразуем DataFrame в список словарей


# Пример использования функции:
operations = read_transactions_xlsx(r"C:\Users\User\pythonProject5.1(0)\data\transactions_excel.xlsx")
print(operations)
