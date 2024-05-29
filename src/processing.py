from datetime import datetime
from typing import List


def sort_by_date(list_of_dicts: List[dict], order: str = "descending") -> List[dict]:
    reverse = order == "descending"
    """
        Сортирует список словарей по ключу 'date' в порядке возрастания или убывания.

        Args:
    - list_of_dicts: Список словарей, содержащих ключ 'date' в виде строки.
    - order: Порядок сортировки, либо 'по возрастанию', либо 'по убыванию'.По умолчанию используется 'по убыванию'

        Возвращает:
        - Отсортированный список словарей по ключу 'date'.
        """
    return sorted(list_of_dicts, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)


# Пример использования
input_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


"""output_descending = sort_by_date(input_data, "descending")
print(output_descending)"""


def filter_by_state(list_of_dicts: List[dict], state: str = "EXECUTED") -> List[dict]:
    """
    Фильтрует список словарей по ключу 'state'.

    Args:
    - list_of_dicts: Список словарей, содержащих ключ 'state' в виде строки.
    - state: Состояние, по которому будет производиться фильтрация. По умолчанию 'EXECUTED'.

    Возвращает:
    - Отфильтрованный список словарей, содержащих указанное 'state'.
    """
    return [item for item in list_of_dicts if item.get("state") == state]


# Пример использования
input_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


output_default = filter_by_state(input_data, "EXECUTED")
output_canceled = filter_by_state(input_data, "CANCELED")


"""print(output_default)
print(output_canceled)"""
