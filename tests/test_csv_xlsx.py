import unittest
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.csv_xlsx import read_transactions_csv, read_transactions_xlsx


def test_read_transactions_csv() -> None:
    """
    Тест для файла с правильным форматом
    """
    file_path = r"C:\Users\User\pythonProject5.1(0)\data\transactions.csv"
    transactions_list = read_transactions_csv(file_path)
    assert isinstance(transactions_list, list)
    assert all(isinstance(transaction, dict) for transaction in transactions_list)


def test_read_transactions_csv_invalid_file() -> None:
    """
    Тест для файла с неправильным форматом
    """
    file_path = "data.txt"
    transactions_list = read_transactions_csv(file_path)
    assert transactions_list == []


@patch("pandas.read_excel")
def test_read_from_xlsx(mock_read_excel: Any) -> None:
    """
    Тестирование функционала чтения транзакций из Excel файла.
    """
    mock_read_excel.return_value = pd.DataFrame({"Date": ["2022-01-01", "2022-02-01"], "Amount": [100.00, 200.00]})
    result = read_transactions_xlsx(r"C:\Users\User\pythonProject5.1(0)\data\transactions_excel.xlsx")
    expected_result = [{"Date": "2022-01-01", "Amount": 100.00}, {"Date": "2022-02-01", "Amount": 200.00}]
    unittest.TestCase().assertEqual(result, expected_result)


if __name__ == "main":
    unittest.main()
