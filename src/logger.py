import logging
from logging import handlers
from pathlib import Path

# Настройка формата логов
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Путь к файлу логов
LOG_FILE = Path("app.log")


def setup_logger(name: str, log_file: Path = LOG_FILE) -> logging.Logger:
    """
    Настраивает логгер для модуля.

    Args:
        name: Название модуля.
        log_file: Путь к файлу логов.

    Returns:
        Логгер для модуля.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Уровень логирования

    # Создание обработчика для записи в файл
    file_handler = handlers.RotatingFileHandler(
        filename=log_file, mode="w", maxBytes=10485760, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Добавление обработчика к логгеру
    logger.addHandler(file_handler)
    return logger


# Создание логгеров для модулей
masks_logger = setup_logger("masks")
utils_logger = setup_logger("utils")
external_api_logger = setup_logger("external_api")