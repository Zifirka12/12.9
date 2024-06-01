import json
import re
from collections import Counter
from typing import Any, Dict, List


def search_transactions(transactions_1: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрация списка словарей, проверяя наличие строки поиска в описании.

        transactions_1 Список словарей с транзакциями.
        search_string Строка поиска.

    Returns Отфильтрованный список словарей с транзакциями.
    """
    return [
        transaction
        for transaction in transactions_1
        if "description" in transaction and re.search(search_string, transaction["description"])
    ]


def categorize_transactions(
    transactions_2: List[Dict[str, Any]], categories_2: Dict[str, List[str]]
) -> Dict[str, int]:
    """
    Подсчет операций в каждой категории, используя заданные ключевые слова.

        transactions_2 Список словарей с транзакциями.
        categories_2 Словарь с категориями и соответствующими ключевыми словами.

    Returns Словарь, где ключи - названия категорий, а значения - количество транзакций, относящихся к каждой категории.
    """
    category_counts_2: Dict[str, int] = Counter()

    for transaction in transactions_2:
        if "description" in transaction:
            for category, keywords in categories_2.items():
                # Проверяем наличие хотя бы одного ключевого слова в описании транзакции
                if any(keyword.lower() in transaction["description"].lower() for keyword in keywords):
                    category_counts_2[category] += 1
                    break  # Выход из цикла по категориям, если найдено совпадение

    return dict(category_counts_2)


# Пример использования:
def read_transactions_from_json(file_path: str) -> Any:
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
# print("Количество операций в каждой категории:", category_counts)

transactions_4 = [
    {"description": "Оплата за интернет"},
    {"description": "Покупка продуктов в магазине"},
    {"description": "Перевод денег другу"},
    {"description": "Оплата за мобильную связь"},
    {"description": "Покупка билетов на концерт"}
]

categories_4 = {
    "Интернет": ["интернет", "онлайн"],
    "Продукты": ["продукты", "магазин"],
    "Другое": ["перевод", "концерт", "билеты"]
}

result = categorize_transactions(transactions_4, categories_4)
print(result)  # Вывод: {'Интернет': 1, 'Продукты': 1, 'Другое': 3}
