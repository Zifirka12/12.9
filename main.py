import re
from typing import Dict, List

from src.csv_xlsx import read_transactions_csv, read_transactions_xlsx
from src.dictionary_handler import search_transactions
from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.utils import read_json_file, sum_amount
from src.widget import convert_date_format, mask_number


def choose_file_format() -> tuple[List[Dict], str]:
    """Запрашивает у пользователя формат файла и возвращает данные транзакций и тип файла.

    Returns:
        tuple[List[Dict], str]: Список словарей с транзакциями и тип файла (json, csv, excel).
    """
    print("Добро пожаловать в программу работы с банковскими транзакциями!")
    file = input("""Выберите формат файла: 1. Json 2. CSV 3. Excel\n""")
    if file == "1":
        print("Для обработки выбран json файл.\n")
        return read_json_file("data/operations.json"), "json"
    elif file == "2":
        print("Для обработки выбран csv файл.\n")
        return read_transactions_csv("data/transactions.csv"), "csv"
    elif file == "3":
        print("Для обработки выбран excel файл.\n")
        return read_transactions_xlsx("data/transactions_excel.xlsx"), "excel"
    else:
        print("Пожалуйста, выберите правильный номер опции.")
        return choose_file_format()


def filter_by_status(data: List[Dict]) -> List[Dict]:
    """Фильтрует список транзакций по заданному статусу.

    Args:
        data (List[Dict]): Список словарей с транзакциями.

    Returns:
        List[Dict]: Отфильтрованный список транзакций.
    """
    print("Выберите статус, по которому необходимо выполнить фильтрацию.")
    status = input("Доступные для сортировки статусы: EXECUTED, CANCELED, PENDING\n")

    if status.upper() not in ("EXECUTED", "CANCELED", "PENDING"):
        print("Некорректный статус, повторите ввод.")
        return filter_by_status(data)

    return filter_by_state(data, status)


def sort_by_date_and_currency(data: List[Dict], file_type: str) -> List[Dict]:
    """Сортирует список транзакций по дате и фильтрует по валюте.

    Args:
        data (List[Dict]): Список словарей с транзакциями.
        file_type (str): Тип файла (json, csv, excel).

    Returns:
        List[Dict]: Отсортированный и отфильтрованный список транзакций.
    """
    to_sort = input("Отсортировать операции по дате? Да/нет \n")
    if to_sort.lower() == "да":
        time = input("По возрастанию или по убыванию?\n")
        if time.lower() == "по возрастанию":
            data = sort_by_date(data)
        elif time.lower() == "по убыванию":
            data = sort_by_date(data, "decreasing")
        else:
            print("Некорректное значение, повторите ввод.")
            return sort_by_date_and_currency(data, file_type)
    elif to_sort.lower() == "нет":
        pass
    else:
        print("Некорректный ответ, повторите ввод.")
        return sort_by_date_and_currency(data, file_type)

    to_sort = input("Выводить только рублевые транзакции? Да/нет \n")
    if to_sort.lower() == "да":
        return filter_by_currency(data, "RUB")
    elif to_sort.lower() == "нет":
        return data
    else:
        print("Некорректный ответ, повторите ввод.")
        return sort_by_date_and_currency(data, file_type)


def filter_by_keyword(data: List[Dict]) -> List[Dict]:
    """Фильтрует список транзакций по ключевому слову в описании.

    Args:
        data (List[Dict]): Список словарей с транзакциями.

    Returns:
        List[Dict]: Отфильтрованный список транзакций.
    """
    to_sort = input("Отсортировать список операций по определённому слову в описании? Да/нет\n")
    if to_sort.lower() == "да":
        to_find = input("Что вы хотели бы найти? \n")
        return search_transactions(data, to_find)
    elif to_sort.lower() == "нет":
        return data
    else:
        print("Некорректный ответ, повторите ввод.")
        return filter_by_keyword(data)


def print_transactions(data: List[Dict]) -> None:
    """Выводит отформатированный список транзакций на консоль.

    Args:
        data (List[Dict]): Список словарей с транзакциями.
    """
    print("Распечатываю список транзакций которые подходят под критерии")
    if data and len(data) != 0:
        print(f"Всего операций в выборке: {len(data)}\n")
        for operation in data:
            print(
                convert_date_format(operation["date"]),
                next(transaction_descriptions(data)),
            )
            if re.search("Перевод", operation["description"]):
                print(mask_number(operation["from"]), " -> ", mask_number(operation["to"]))
            else:
                print(mask_number(operation["to"]))
                print(f"Сумма: {sum_amount(operation)}руб. \n")
    else:
        print("Не найдено ни одной транзакции подходящей под ваши условия фильтрации")


def main() -> None:
    """Главная функция программы, запускающая обработку транзакций."""
    data, file_type = choose_file_format()
    data = filter_by_status(data)
    data = sort_by_date_and_currency(data, file_type)
    data = filter_by_keyword(data)
    print_transactions(data)


if __name__ == "__main__":
    main()
