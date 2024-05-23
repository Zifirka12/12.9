import csv
from typing import Dict, List

import pandas as pd


def read_transactions_csv(file_path: str) -> list:
    if file_path.endswith(".csv"):
        """
        read_transactions_csv возвращает список словарей
        """
        df = pd.read_csv(file_path, encoding="utf-8")
        transactions_list = df.to_dict(orient="records")
        return transactions_list
    else:
        print("Неверный формат файла CSV.")
        return []


def read_transactions_xlsx(file_path: str) -> List[Dict]:
    """
    Чтение финансовых операций из XLSX-файла.
    """
    opera_1 = pd.read_excel(file_path)  # Читаем файл Excel с помощью Pandas
    return opera_1.to_dict("records")  # Преобразуем DataFrame в список словарей


# Пример использования функции:
operations = read_transactions_xlsx("../data/transactions_excel.xlsx")
print(operations)
