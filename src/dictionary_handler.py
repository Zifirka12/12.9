import json
import re
from typing import Any, Dict, List
from collections import Counter


def search_transactions(transactions_1: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрация списка словарей, проверяя наличие строки поиска в описании.

    Args:
        transactions_1 (List[Dict[str, Any]]): Список словарей с транзакциями.
        search_string (str): Строка поиска.

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список словарей с транзакциями, где в описании 
        содержится строка поиска.
    """
    return [
        transaction
        for transaction in transactions_1
        if "description" in transaction and re.search(search_string, transaction["description"])
    ]


def categorize_transactions(transactions_2: List[Dict[str, Any]], categories_2: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Подсчет операций в каждой категории, используя заданные ключевые слова.

    Args:
        transactions_2 (List[Dict[str, Any]]): Список словарей с транзакциями.
        categories_2 (Dict[str, List[str]]): Словарь с категориями и соответствующими ключевыми словами.

    Returns:
        Dict[str, int]: Словарь, где ключи - названия категорий, а значения - количество 
        транзакций, относящихся к каждой категории.
    """
    category_counts_2 = Counter()
    for transaction in transactions_2:
        if "description" in transaction:
            for category, keywords in categories_2.items():
                if any(keyword in transaction["description"] for keyword in keywords):
                    category_counts_2[category] += 1
                    break
    return dict(category_counts_2)


# Пример использования:
def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Чтение транзакций из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями из JSON-файла.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


transactions = read_transactions_from_json("data/operations.json")

categories = {"Перевод": ["Перевод организации", "Перевод частному лицу"]}

category_counts = categorize_transactions(transactions, categories)
print("Количество операций в каждой категории:", category_counts)

transactions_3 = [
    {"description": "Перевод организации"},
    {"description": "Покупка товаров"},
    {"description": "Оплата услуг"},
    {"description": "Перевод частному лицу"},
]

categories_3 = {
    "Перевод": ["Перевод организации", "Перевод частному лицу"],
    "Покупка": ["Покупка товаров"],
    "Оплата": ["Оплата услуг"],
}

category_counts = categorize_transactions(transactions_3, categories_3)
print(category_counts)  # Вывод: {'Перевод': 2, 'Покупка': 1, 'Оплата': 1}
