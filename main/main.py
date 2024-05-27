import csv
import json
from datetime import datetime
from os import name
from typing import Any

import openpyxl


def get_transactions_from_json(file_path: str) -> Any:
    """
    Функция для получения информации о транзакциях из JSON файла.
    Args:
        file_path (str): Путь к JSON файлу.
    Returns:
        list: Список словарей с данными о транзакциях.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transactions = json.load(f)
        return transactions
    except FileNotFoundError:
        raise Exception(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    except json.JSONDecodeError:
        raise Exception(f"Ошибка декодирования JSON файла {file_path}. Проверьте корректность формата файла.")


def get_transactions_from_csv(file_path: str) -> list:
    """
    Функция для получения информации о транзакциях из CSV файла.
    Args:
        file_path (str): Путь к CSV файлу.
    Returns:
        list: Список словарей с данными о транзакциях.
    """
    transactions = []
    try:
        with open(file_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
        return transactions
    except FileNotFoundError:
        raise Exception(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    except csv.Error as e:
        raise Exception(f"Ошибка чтения CSV файла {file_path}: {e}")


def get_transactions_from_xlsx(file_path: str) -> Any:
    """
    Функция для получения информации о транзакциях из XLSX файла.
    Args:
    file_path (str): Путь к XLSX файлу.
    Returns:
    list: Список словарей с данными о транзакциях.
    """
    transactions = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active
        headers = [cell.value for cell in worksheet[1]]
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            transaction = {headers[i]: cell for i, cell in enumerate(row)}
            transactions.append(transaction)
        return transactions
    except FileNotFoundError:
        raise Exception(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    except Exception as e:
        raise Exception(f"Ошибка чтения XLSX файла {file_path}: {e}")


def parse_date(date_str: str) -> datetime:
    """
    Парсит строку с датой в объект datetime.
    Args:
        date_str (str): Строка с датой.
    Returns:
        datetime: Объект datetime.
    """
    return datetime.strptime(date_str, "%d.%m.%Y")


def format_date(date_obj: datetime) -> str:
    """
    Форматирует объект datetime обратно в строку.
    Args:
        date_obj (datetime): Объект datetime.
    Returns:
        str: Строка с датой.
    """
    return date_obj.strftime("%d.%m.%Y")


def filter_transactions_by_currency(transactions: list) -> list:
    return [transaction for transaction in transactions if transaction.get("currency") == "RUB"]


def filter_transactions_by_description(transactions: list, word: str) -> list:
    return [transaction for transaction in transactions if word.lower() in transaction.get("description", "").lower()]


def sort_transactions_by_date(transactions: list, order: str = "asc") -> list:
    """
    Сортирует транзакции по дате.
    Args:
        transactions (list): Список транзакций.
        order (str): Порядок сортировки ('asc' или 'desc').
    Returns:
        list: Отсортированный список транзакций.
    """
    for transaction in transactions:
        # Предполагается, что дата находится в ключе 'date'
        transaction["date"] = parse_date(transaction["date"])

    sorted_transactions = sorted(transactions, key=lambda x: x["date"], reverse=(order == "desc"))

    for transaction in sorted_transactions:
        transaction["date"] = format_date(transaction["date"])

    return sorted_transactions


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    file_path = get_file_path()
    transactions = get_transactions(file_path)
    if transactions:
        transactions = filter_transactions(transactions)
        transactions = sort_transactions(transactions)
        print_transactions(transactions)
    else:
        print("Информация о транзакциях не получена.")


def get_file_path() -> str:
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из json файла")
    print("2. Получить информацию о транзакциях из csv файла")
    print("3. Получить информацию о транзакциях из xlsx файла")
    choice = input("Введите номер пункта меню: ")
    if choice == "1":
        return input("Введите путь к json файлу: ")
    elif choice == "2":
        return input("Введите путь к csv файлу: ")
    elif choice == "3":
        return input("Введите путь к xlsx файлу: ")
    else:
        print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
        return get_file_path()


def get_transactions(file_path: str) -> Any:
    file_extension = file_path.split(".")[-1]
    if file_extension == "json":
        return get_transactions_from_json(file_path)
    elif file_extension == "csv":
        return get_transactions_from_csv(file_path)
    elif file_extension == "xlsx":
        return get_transactions_from_xlsx(file_path)
    else:
        print(f"Неизвестный формат файла: {file_extension}")
        return []


def filter_transactions(transactions: list) -> list:
    status = input(
        "Введите статус по которому необходимо выполнить фильтрацию."
        " \nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
    ).upper()
    currency = input("Выводить только рублевые транзакции? Да/Нет\n").lower() == "да"
    word = input("Введите слово для фильтрации:\n")

    return [
        transaction
        for transaction in transactions
        if transaction.get("status") == status
        and (not currency or transaction.get("currency") == "RUB")
        and word.lower() in transaction.get("description", "").lower()
    ]


def sort_transactions(transactions: list) -> list:
    sort_by_date = input("Отсортировать операции по дате? Да/Нет\n").lower() == "да"
    order = input("Отсортировать по возрастанию или по убыванию?\n")
    while order.lower() not in ["по возрастанию", "по убыванию"]:
        print("Неверный порядок сортировки. Введите 'по возрастанию' или 'по убыванию'.")
        order = input("Отсортировать по возрастанию или по убыванию?\n")

    if sort_by_date:
        return sort_transactions_by_date(transactions, order)
    else:
        return transactions


def print_transactions(transactions: list) -> None:
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for transaction in transactions:
        print(f"{transaction['date']} {transaction['description']}")
        print(f"Счет {transaction['account']}")
        print(f"Сумма: {transaction['amount']} {transaction['currency']}\n")

        # Добавление логики в основную часть программы
        if transactions:
            # Фильтрация по статусу
            status = input(
                "Введите статус по которому необходимо выполнить фильтрацию."
                " \nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            )
            transactions = [transaction for transaction in transactions if transaction.get("status") == status]

            # Сортировка по дате
            sort_by_date = input("Отсортировать операции по дате? Да/Нет\n").lower()
            if sort_by_date == "да":
                order = input("Отсортировать по возрастанию или по убыванию?\n")
                while order.lower() not in ["по возрастанию", "по убыванию"]:
                    print("Неверный порядок сортировки. Введите 'по возрастанию' или 'по убыванию'.")
                    order = input("Отсортировать по возрастанию или по убыванию?\n")
                transactions = sort_transactions_by_date(transactions, order)

# Фильтрация по валюте
            filter_by_currency = input("Выводить только рублевые транзакции? Да/Нет\n").lower()
            if filter_by_currency == "да":
                transactions = filter_transactions_by_currency(transactions)

            # Фильтрация по описанию
            filter_by_description = input(
                "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
            ).lower()
            if filter_by_description == "да":
                word = input("Введите слово для фильтрации:\n")
                transactions = filter_transactions_by_description(transactions, word)

            # Вывод результата
            print_transactions(transactions)
        else:
            print("Информация о транзакциях не получена.")


if name == "main":
    main()
