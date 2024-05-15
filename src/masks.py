from logger import masks_logger


def mask_card(card_number: str) -> str:
    """
    Функция принимает на вход номер карты и возвращает ее маску.
    """
    if len(card_number) == 16:  # Проверяем длину номера карты
        masked_card = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        return masked_card
    return "Некорректный номер карты"


def mask_account(account_number: str) -> str:
    """
    Функция принимает на вход номер счета и возвращает его маску.
    """
    if len(account_number) > 4:  # Проверяем, что номер счета хотя бы 4 символа
        masked_account = "**" + account_number[-4:]
        return masked_account
    return "Некорректный номер счета"


masks_logger.debug("Это отладочное сообщение из модуля masks")
masks_logger.error("Это сообщение об ошибке из модуля masks")
