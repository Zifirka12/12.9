import json
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

from src.external_API import get_currency_rate
from src.logger import setup_logging

logger = setup_logging()


def read_json_file(file_path: Path) -> List[Dict[str, Any]]:
    """Считывает транзакции из JSON-файла."""
    try:
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка при чтении JSON-файла: {e}")
        return []


def sum_amount(transaction: dict) -> float:
    """Суммирует суммы всех транзакций"""
    total = 0.0
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
    amount = float(transaction.get("operationAmount", {}).get("amount", 0.0))

    if currency == "RUB":
        total += amount
    elif currency == "EUR":
        total += amount * get_currency_rate("EUR")
    elif currency == "USD":
        total += amount * get_currency_rate("USD")
    else:
        logger.warning(f"Неизвестная валюта: {currency}")

    logger.info(f"Сумма транзакции: {total:.2f} RUB")
    return total


if __name__ == "__main__":
    operations_path = Path("../data/operations.json")  # Путь к файлу с операциями
    transactions = read_json_file(operations_path)
    total_rub = sum_amount(
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
    print(f"Общая сумма в рублях: {total_rub:.2f}")
