"""Message formatting utilities"""
from typing import Dict, Any
from bot.config import EVENT_NAME, EVENT_DATE, EVENT_VENUE
from bot.services.quiz_data import TAG_LABELS, TAG_TECHNIQUES


def format_welcome_message(first_name: str) -> str:
    """Format welcome message"""
    return f"""🧠 Добро пожаловать в «{EVENT_NAME}», {first_name}!

Пройдите 3-минутный квиз и узнайте, на сколько процентов
работает ваш мозг — и получите персональный гайд
«5 нейротехник для продуктивности».

📊 7 вопросов • ⏱ 3 минуты • 📄 PDF-гайд в подарок"""


def format_result_message(quiz_result: Dict[str, Any]) -> str:
    """Format quiz result message"""
    total_score = quiz_result.get('total_score', 0)
    profile = quiz_result.get('profile', '')
    main_tag = quiz_result.get('main_tag', 'focus')

    # Get profile emoji
    if profile == "Нейроновичок":
        profile_emoji = "🌱"
        description = "Вашему мозгу срочно нужна перезагрузка. Мероприятие даст вам конкретные инструменты."
    elif profile == "Нейропрактик":
        profile_emoji = "⚡"
        description = "У вас хорошая база, но есть точки роста. Вы получите продвинутые техники."
    else:  # Нейромастер
        profile_emoji = "🏆"
        description = "Впечатляющий результат! Мероприятие поможет выйти на новый уровень."

    tag_label = TAG_LABELS.get(main_tag, main_tag)
    tag_technique = TAG_TECHNIQUES.get(main_tag, "")

    return f"""📊 <b>Ваш результат:</b> {total_score}/24

🏷 <b>Профиль:</b> {profile_emoji} {profile}

{description}

🎯 <b>Ваш приоритет:</b> {tag_label}
💡 {tag_technique}

━━━━━━━━━━━━━━━━━━━━━

📄 Ваш персональный гайд готов! Сейчас отправлю...

💡 Хотите узнать больше? {EVENT_DATE} в {EVENT_VENUE}
пройдёт мероприятие «{EVENT_NAME}» — живые
мастер-классы от нейрофизиологов."""


def format_help_message() -> str:
    """Format help message"""
    return """❓ <b>Справка по боту</b>

<b>Доступные команды:</b>
/start — Начать работу с ботом
/quiz — Запустить квиз
/result — Показать последний результат
/help — Эта справка

<b>Как это работает:</b>
1. Пройдите короткий квиз из 7 вопросов
2. Получите анализ вашего когнитивного профиля
3. Скачайте персональный PDF-гайд
4. Забронируйте место на мероприятии

💬 После прохождения квиза вы можете писать сообщения
в этот чат — наши менеджеры ответят вам."""


def format_question_message(question_num: int, total_questions: int, question_text: str) -> str:
    """Format quiz question message"""
    return f"❓ <b>Вопрос {question_num} из {total_questions}</b>\n\n{question_text}"
