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
        if re.findall(search_string.lower(), row["description"].lower()):
            result.append(row)
    return result


def categorize_operations(data: List[Dict[str, str]], categories: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Функция принимает список словарей с данными о банковских операциях и словарь категорий операций.
    Возвращает словарь, где ключи - это названия категорий, а значения - количество операций в каждой категории.
    """
    category_count = defaultdict(int)

    for row in data:
        for operation in data:
            if operation['description'] == row:
                category_count[operation] += 1

    return category_count
