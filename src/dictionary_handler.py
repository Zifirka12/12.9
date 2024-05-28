import re
from collections import defaultdict
from typing import DefaultDict, Dict, List


def search_operations(data_1: List[Dict[str, str]], search_string_1: str) -> List[Dict[str, str]]:
    """
    Функция принимает список словарей с данными о банковских операциях и строку поиска.
    Возвращает список словарей, у которых в описании есть данная строка.
    """
    result = []
    for row in data_1:
        if re.findall(search_string_1.lower(), row["description"].lower()):
            result.append(row)
    return result


def categorize_operations(data_2: List[Dict[str, str]]) -> defaultdict[str, int]:
    """
    Функция принимает список словарей с данными о банковских операциях и словарь категорий операций.
    Возвращает словарь, где ключи - это названия категорий, а значения - количество операций в каждой категории.
    """
    category_count: DefaultDict[str, int] = defaultdict(int)

    for row in data_2:
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in row["description"].lower():
                    category_count[category] += 1

    return category_count


# Данные о банковских операциях
data = [
    {"description": "Покупка продуктов в магазине", "amount": "1000"},
    {"description": "Оплата за интернет", "amount": "500"},
    {"description": "Зарплата", "amount": "2000"},
    {"description": "Оплата коммунальных услуг", "amount": "1500"},
    {"description": "Покупка билетов в кино", "amount": "800"}
]

# Словарь категорий операций
categories = {
    "покупки": ["Покупка", "Покупки", "Билеты"],
    "оплата услуг": ["Оплата", "Коммунальные"],
    "доход": ["Зарплата"]
}

search_string = "покупка"
result_search = search_operations(data, search_string)
print(result_search)

result_categorize = categorize_operations(data)
print(result_categorize)
