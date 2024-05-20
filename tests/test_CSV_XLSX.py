from src.CSV_XLSX import read_transactions_xlsx, read_transactions_csv, read_transactions
import pandas as pd

from unittest.mock import patch
import unittest


class Transaction:
    """Представляет финансовую операцию."""

    def __init__(self, date: str, description: str, amount: float):
        self.date = date
        self.description = description
        self.amount = amount

    def __str__(self):
        return f"Дата: {self.date}, Описание: {self.description}, Сумма: {self.amount}"


class TestReadTransactions(unittest.TestCase):
    """Тесты для считывания транзакций из CSV и XLSX файлов."""

    @patch('pandas.read_excel')
    def test_read_transactions_xlsx(self, mock_read_excel):
        """Тестирует считывание транзакций из XLSX-файла."""
        mock_read_excel.return_value = pd.DataFrame(
            {
                'Date': ['2023-10-26', '2023-10-27'],
                'Description': ['Salary', 'Groceries'],
                'Amount': [2500.00, 150.00],
            }
        )
        file_path = 'transactions_excel.xlsx'
        transactions = read_transactions_xlsx(file_path)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].date, '2023-10-26')
        self.assertEqual(transactions[0].description, 'Salary')
        self.assertEqual(transactions[0].amount, 2500.00)
        self.assertEqual(transactions[1].date, '2023-10-27')
        self.assertEqual(transactions[1].description, 'Groceries')
        self.assertEqual(transactions[1].amount, 150.00)

    @patch('builtins.open')
    def test_read_transactions_csv(self, mock_open):
        """Тестирует считывание транзакций из CSV-файла."""
        """вот он пока не работает"""
        mock_file = mock_open.return_value.enter.return_value
        mock_file.read.return_value = """Date,Description,Amount
        2023-10-26,Salary,2500.00
        2023-10-27,Groceries,150.00"""
        file_path = 'transactions.csv'
        transactions = read_transactions_csv(file_path)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].date, '2023-10-26')
        self.assertEqual(transactions[0].description, 'Salary')
        self.assertEqual(transactions[0].amount, 2500.00)
        self.assertEqual(transactions[1].date, '2023-10-27')
        self.assertEqual(transactions[1].description, 'Groceries')
        self.assertEqual(transactions[1].amount, 150.00)

    def test_read_transactions_invalid_file(self):
        """Тестирует считывание транзакций из некорректного файла."""
        file_path = 'transactions.txt'
        transactions = read_transactions(file_path)
        self.assertIsNone(transactions)


if __name__ == '__main__':
    unittest.main()
