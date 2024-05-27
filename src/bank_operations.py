import json
import csv
import openpyxl


def get_transactions_from_json(file_path):
    """
    Функция для получения информации о транзакциях из JSON файла.
    Args:
        file_path (str): Путь к JSON файлу.
    Returns:
        list: Список словарей с данными о транзакциях.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
        return transactions
    except FileNotFoundError:
        raise Exception(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    except json.JSONDecodeError:
        raise Exception(f"Ошибка декодирования JSON файла {file_path}. Проверьте корректность формата файла.")

def get_transactions_from_csv(file_path):
    """
    Функция для получения информации о транзакциях из CSV файла.
    Args:
        file_path (str): Путь к CSV файлу.
    Returns:
        list: Список словарей с данными о транзакциях.
    """
    transactions = []
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
        return transactions
    except FileNotFoundError:
        raise Exception(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    except csv.Error as e:
        raise Exception(f"Ошибка чтения CSV файла {file_path}: {e}")

def get_transactions_from_xlsx(file_path):
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
        for row in worksheet.iter_rows(min_row=2):
            transaction = {headers[i]: cell.value for i, cell in enumerate(row)}
            transactions.append(transaction)
        return transactions
    except FileNotFoundError:
        raise Exception(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    except Exception as e:
        raise Exception(f"Ошибка чтения XLSX файла {file_path}: {e}")

# Определения функций sort_transactions_by_date, filter_transactions_by_currency и filter_transactions_by_description

def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из json файла")
    print("2. Получить информацию о транзакциях из csv файла")
    print("3. Получить информацию о транзакциях из xlsx файла")
    choice = input("Введите номер пункта меню: ")
    transactions = []
    if choice == '1':
        file_path = input("Введите путь к json файлу: ")
        transactions = get_transactions_from_json(file_path)
    elif choice == '2':
        file_path = input("Введите путь к csv файлу: ")
        transactions = get_transactions_from_csv(file_path)
    elif choice == '3':
        file_path = input("Введите путь к xlsx файлу: ")
        transactions = get_transactions_from_xlsx(file_path)
    else:
        print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
    if transactions:
        # Функции для сортировки и фильтрации
        def sort_transactions_by_date(transactions, order='asc'):
            return sorted(transactions, key=lambda x: x['date'], reverse=(order == 'desc'))

        def filter_transactions_by_currency(transactions, currency='RUB'):
            return [transaction for transaction in transactions if transaction.get('currency') == currency]

        def filter_transactions_by_description(transactions, word):
            return [transaction for transaction in transactions if
                    word.lower() in transaction.get('description', '').lower()]

        def print_transactions(transactions):
            print(f"Всего банковских операций в выборке: {len(transactions)}")
            for transaction in transactions:
                print(f"{transaction['date']} {transaction['description']}")
                print(f"Счет {transaction['account']}")
                print(f"Сумма: {transaction['amount']} {transaction['currency']}\n")

        # Добавление логики в основную часть программы
        if transactions:
            # Фильтрация по статусу
            status = input(
                "Введите статус по которому необходимо выполнить фильтрацию. \nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n")
            transactions = [transaction for transaction in transactions if transaction.get('status') == status]

            # Сортировка по дате
            sort_by_date = input("Отсортировать операции по дате? Да/Нет\n").lower()
            if sort_by_date == "да":
                order = input("Отсортировать по возрастанию или по убыванию?\n")
                while order.lower() not in ['по возрастанию', 'по убыванию']:
                    print("Неверный порядок сортировки. Введите 'по возрастанию' или 'по убыванию'.")
                    order = input("Отсортировать по возрастанию или по убыванию?\n")
                transactions = sort_transactions_by_date(transactions, order)

            # Фильтрация по валюте
            filter_by_currency = input("Выводить только рублевые транзакции? Да/Нет\n").lower()
            if filter_by_currency == "да":
                transactions = filter_transactions_by_currency(transactions)

            # Фильтрация по описанию
            filter_by_description = input(
                "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").lower()
            if filter_by_description == "да":
                word = input("Введите слово для фильтрации:\n")
                transactions = filter_transactions_by_description(transactions, word)

            # Вывод результата
            print_transactions(transactions)
        else:
            print("Информация о транзакциях не получена.")


if __name__ == "__main__":
    main()
