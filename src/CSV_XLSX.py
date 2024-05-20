import csv
from typing import List, Union
import pandas as pd


class Transaction:
    """Представляет финансовую операцию."""

    def __init__(self, date: str, description: str, amount: float):
        self.date = date
        self.description = description
        self.amount = amount

    def __str__(self):
        return f"Дата: {self.date}, Описание: {self.description}, Сумма: {self.amount}"


def read_transactions_csv(file_path: str) -> List[Transaction]:
    """Считывает транзакции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        List[Transaction]: Список транзакций.
    """
    transactions = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transaction = Transaction(
                row['Date'], row['Description'], float(row['Amount'])
            )
            transactions.append(transaction)
    return transactions


def read_transactions_xlsx(file_path: str) -> List[Transaction]:
    """Считывает транзакции из XLSX-файла.

    Args:
        file_path (str): Путь к XLSX-файлу.

    Returns:
        List[Transaction]: Список транзакций.
    """
    df = pd.read_excel(file_path)
    transactions = []
    for index, row in df.iterrows():
        transaction = Transaction(
            row['Date'], row['Description'], row['Amount']
        )
        transactions.append(transaction)
    return transactions


def read_transactions(file_path: str) -> Union[List[Transaction], None]:
    """Считывает транзакции из файла, определяя тип файла по расширению.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        Union[List[Transaction], None]: Список транзакций, если считывание прошло успешно, иначе None.
    """
    if file_path.endswith('.csv'):
        return read_transactions_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return read_transactions_xlsx(file_path)
    else:
        return None
