"""Main reply keyboards"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Пройти квиз")],
            [KeyboardButton(text="📈 Мой результат"), KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True
    )
