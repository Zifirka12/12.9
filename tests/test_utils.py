import json
import os
from pathlib import Path
from unittest.mock import MagicMock, Mock, mock_open, patch

"""# Импортируем Mock и patch для создания заглушек"""

import requests
from dotenv import load_dotenv

from src.external_API import get_currency_rate
from src.utils import read_json_file, sum_amount

load_dotenv()
API_KEY = os.getenv("api_key")

"""# Тест функции get_transaction_rub при ошибке API"""


@patch("requests.get")  # Заменяем функцию requests.get заглушкой
def test_get_transaction_rub_api_error(mock_get: Mock) -> None:
    """# Создаем заглушку ответа, которая будет вызывать исключение при проверке статуса"""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
    mock_get.return_value = mock_response  # Возвращаем заглушку ответа при вызове requests.get

    # Проверяем, что функция возвращает 1.0 при ошибке API
    result = get_currency_rate("USD")
    assert result == 1.0


@patch("requests.get")
def test_get_transaction_rub_api_success(mock_get: MagicMock) -> None:
    mock_get.return_value.json.return_value = {"rates": {"RUB": 75.0}}
    t = {"amount": 100, "currency": "USD"}
    assert get_currency_rate(t) == 75.0


"""# Тест функции read_transactions при успешном чтении файла"""


@patch("builtins.open", create=True)
def test_read_transactions_success(mock_open: MagicMock) -> None:
    # Создаем тестовые данные
    test_data = [{"amount": 100, "currency": "RUB"}]
    # Подготавливаем мокированный файл с помощью mock_open
    mock_open.return_value.read.return_value = json.dumps(test_data)
    # Проверяем, что функция возвращает правильный список транзакций
    result = read_json_file(Path("test_transactions.json"))
    assert result == []


"""# Тест функции read_transactions при чтении пустого файла"""


def test_read_transactions_empty_file() -> None:
    # Создаем пустой файл
    with open("test_transactions.json", "w") as f:
        pass

    """# Проверяем, что функция возвращает пустой список"""
    result = read_json_file(Path("test_transactions.json"))
    assert result == []

    os.remove("test_transactions.json")  # Удаляем тестовый файл

    """
    Тестирует функцию sum_amount, которая должна возвращать сумму из операции.
    Проверяет, что функция sum_amount корректно извлекает сумму из предоставленного словаря,
    содержащего информацию об операции. Ожидается, что функция вернет сумму 31957.58.
    """


def test_sum_amount() -> None:
    assert (
        sum_amount(
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            }
        )
        == 31957.58
    )
