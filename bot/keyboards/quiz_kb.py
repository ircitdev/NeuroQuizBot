"""Quiz inline keyboards"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models import QuizQuestion


def get_quiz_keyboard(question: QuizQuestion) -> InlineKeyboardMarkup:
    """
    Generate inline keyboard for quiz question

    Args:
        question: QuizQuestion object

    Returns:
        InlineKeyboardMarkup with answer options
    """
    buttons = []

    for idx, option in enumerate(question.options):
        # Callback format: quiz:question_id:option_index
        callback_data = f"quiz:{question.id}:{idx}"
        buttons.append([
            InlineKeyboardButton(
                text=option.label,
                callback_data=callback_data
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_start_quiz_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for starting the quiz"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать квиз", callback_data="start_quiz")]
    ])


def get_event_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard with event registration buttons"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎟 Забронировать место", url="https://t.me/your_event_link")],
        [InlineKeyboardButton(text="🌐 Подробнее о мероприятии", url="https://your-event-website.com")],
    ])
