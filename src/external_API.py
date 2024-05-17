import os
from typing import Any

import requests
from dotenv import load_dotenv

from src.logger import setup_logging

logger = setup_logging()


load_dotenv()
API_KEY = os.getenv("api_key")


def get_currency_rate(currency: Any) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    try:
        response = requests.get(url, headers={"apikey": API_KEY}, timeout=5)
        response.raise_for_status()  # Поднимает исключение, если код ответа не 2xx
        response_data = response.json()
        rate = response_data["rates"]["RUB"]
        if rate:
            logger.info(f"Курс {currency}/RUB: {rate}")
            return float(rate)
        else:
            logger.error(f"Курс {currency}/RUB не найден в ответе API")
            return 1.0
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API при получении курса {currency}/RUB: {e}")
        return 1.0
