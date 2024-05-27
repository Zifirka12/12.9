from typing import List, Dict
import re
from collections import defaultdict


def search_operations(data: List[Dict[str, str]], search_string: str) -> List[Dict[str, str]]:
    """
    Функция принимает список словарей с данными о банковских операциях и строку поиска.
    Возвращает список словарей, у которых в описании есть данная строка.
    """
    result = []
    for row in data:
        if re.search(search_string, row['description'], re.IGNORECASE):
            result.append(row)
    return result


def categorize_operations(data: List[Dict[str, str]], categories: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Функция принимает список словарей с данными о банковских операциях и словарь категорий операций.
    Возвращает словарь, где ключи - это названия категорий, а значения - количество операций в каждой категории.
    """
    category_count = defaultdict(int)

    for row in data:
        for category, keywords in categories.items():
            for keyword in keywords:
                if re.search(keyword, row['description'], re.IGNORECASE):
                    category_count[category] += 1

    return category_count
