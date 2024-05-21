import os
import unittest
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.CSV_XLSX import read_transactions, read_transactions_csv, read_transactions_xlsx


class Transaction:
    """Представляет финансовую операцию."""

    def init(self, date: str, description: str, amount: float):
        self.date = date
        self.description = description
        self.amount = amount

    def str(self) -> str:
        return f"Дата: {self.date}, Описание: {self.description}, Сумма: {self.amount}"


class TestReadTransactions(unittest.TestCase):
    """Тесты для считывания транзакций из CSV и XLSX файлов."""

    @patch("pandas.read_excel")
    def test_read_transactions_xlsx(self, mock_read_excel: Any) -> None:
        """Тестирует считывание транзакций из XLSX-файла."""
        mock_read_excel.return_value = pd.DataFrame(
            {
                "Date": ["2023-10-26", "2023-10-27"],
                "Description": ["Salary", "Groceries"],
                "Amount": [2500.00, 150.00],
            }
        )
        file_path = "transactions_excel.xlsx"
        transactions = read_transactions_xlsx(file_path)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].date, "2023-10-26")
        self.assertEqual(transactions[0].description, "Salary")
        self.assertEqual(transactions[0].amount, 2500.00)
        self.assertEqual(transactions[1].date, "2023-10-27")
        self.assertEqual(transactions[1].description, "Groceries")
        self.assertEqual(transactions[1].amount, 150.00)

    def test_read_transactions_csv(self) -> None:
        """Тестирует считывание транзакций из CSV-файла."""
        current_dir = os.path.dirname(__file__)  # Получаем путь к текущей директории
        file_path = os.path.join(current_dir, "../transactions.csv")  # Собираем полный путь к файлу

        transactions = read_transactions_csv(file_path)

        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].date, "2023-10-26")
        self.assertEqual(transactions[0].description, "Salary")
        self.assertEqual(transactions[0].amount, 2500.00)
        self.assertEqual(transactions[1].date, "2023-10-27")
        self.assertEqual(transactions[1].description, "Groceries")
        self.assertEqual(transactions[1].amount, 150.00)

    def test_read_transactions_invalid_file(self) -> None:
        """Тестирует считывание транзакций из некорректного файла."""
        file_path = "transactions.txt"
        transactions = read_transactions(file_path)
        self.assertIsNone(transactions)


if __name__ == "main":
    unittest.main()
