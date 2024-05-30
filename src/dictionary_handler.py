import json
import re
from typing import Any


def search_transactions(transactions_1: Any, search_string: Any) -> list:
    """Фильтрация списка словарей, проверяя наличие строки поиска в описании"""
    return [
        transaction
        for transaction in transactions_1
        if "description" in transaction and re.search(search_string, transaction["description"])
    ]


def categorize_transactions(transactions_2: Any, categories_2: Any) -> dict[Any, int]:
    category_counts_1 = {category: 0 for category in categories_2.keys()}
    """Создание словаря для подсчета операций,Подсчет операций в каждой категории"""
    for transaction in transactions_2:
        if "description" in transaction:
            for category, keywords in categories_2.items():
                if any(keyword in transaction["description"] for keyword in keywords):
                    category_counts_1[category] += 1
                    break
    return category_counts_1


""" Пример использования:"""
def read_transactions_from_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


transactions = read_transactions_from_json("../data/operations.json")

categories = {"Перевод": ["Перевод организации", "Перевод частному лицу"]}

category_counts = categorize_transactions(transactions, categories)
print("Количество операций в каждой категории:", category_counts)
