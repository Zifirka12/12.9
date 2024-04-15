from src.masks import mask_account, mask_card

"""
# Проверка функции mask_card() с аннотациями типов
"""
# Проверка функции mask_card() с аннотациями типов
def test_mask_card() -> str:
    assert mask_card("1234567890123456") == "1234 56** **** 3456"
    assert mask_card("12345") == "Некорректный номер карты"

"""
# Проверка функции mask_account() с аннотациями типов
"""
def test_mask_account() -> str:
    assert mask_account("73654108430135874305") == "**4305"
    assert mask_account("123") == "Некорректный номер счета"
