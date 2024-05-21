import unittest
from unittest.mock import patch
import pandas as pd
from typing import Any
from src.CSV_XLSX import read_transactions_csv, read_transactions_xlsx


@patch("csv.DictReader")
def test_read_from_csv(mock_csv_reader: Any) -> None:
    """
        Тестирование функционала чтения транзакций из CSV файла.

        Args:
            mock_csv_reader (Any): Мок-объект для имитации csv.DictReader.
        """
    mock_csv_reader.return_value = iter(
        [{"Date": "2022-01-01", "Amount": "100.00"}, {"Date": "2022-02-01", "Amount": "200.00"}]
    )
    result = read_transactions_csv(r"C:\Users\User\pythonProject5.1(0)\data\transactions.csv")
    expected_result = [{"Date": "2022-01-01", "Amount": "100.00"}, {"Date": "2022-02-01", "Amount": "200.00"}]
    unittest.TestCase().assertEqual(result, expected_result)


@patch("pandas.read_excel")
def test_read_from_xlsx(mock_read_excel: Any) -> None:
    """
    Тестирование функционала чтения транзакций из Excel файла.

    Args:
        mock_read_excel (Any): Мок-объект для имитации pandas.read_excel.
    """
    mock_read_excel.return_value = pd.DataFrame({"Date": ["2022-01-01", "2022-02-01"], "Amount": [100.00, 200.00]})
    result = read_transactions_xlsx(r"C:\Users\User\pythonProject5.1(0)\data\transactions_excel.xlsx")
    expected_result = [{"Date": "2022-01-01", "Amount": 100.00}, {"Date": "2022-02-01", "Amount": 200.00}]
    unittest.TestCase().assertEqual(result, expected_result)


if __name__ == "main":
    unittest.main()
