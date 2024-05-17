import logging
from typing import Any


def setup_logging() -> Any:
    """Настраивает логирование."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Исправленное имя файла
    file_handler = logging.FileHandler("app.log", mode="w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)

    return logger
