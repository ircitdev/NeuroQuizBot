"""Forum topic management for CRM supergroup"""
from typing import Dict, Any
from datetime import datetime
from aiogram import Bot
from bot.config import SUPERGROUP_CHAT_ID
from bot.services.quiz_data import TAG_LABELS


async def create_lead_topic(bot: Bot, user_data: Dict[str, Any], quiz_result: Dict[str, Any]) -> int:
    """
    Create a forum topic in supergroup for the lead

    Args:
        bot: Bot instance
        user_data: User data dict
        quiz_result: Quiz result dict

    Returns:
        thread_id: Forum thread ID
    """
    # Create topic name
    name = user_data.get("first_name", "Аноним")
    username = user_data.get("username", "")
    topic_name = f"🧠 {name}"
    if username:
        topic_name += f" (@{username})"

    # Truncate to 128 chars (Telegram limit)
    topic_name = topic_name[:128]

    # Create forum topic
    result = await bot.create_forum_topic(
        chat_id=SUPERGROUP_CHAT_ID,
        name=topic_name
    )

    thread_id = result.message_thread_id

    # Send lead card to topic
    card = format_lead_card(user_data, quiz_result)
    await bot.send_message(
        chat_id=SUPERGROUP_CHAT_ID,
        message_thread_id=thread_id,
        text=card,
        parse_mode="HTML"
    )

    return thread_id


def format_lead_card(user_data: Dict[str, Any], quiz_result: Dict[str, Any]) -> str:
    """Format lead information card for CRM"""
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    username = user_data.get("username", "")
    user_id = user_data.get("tg_user_id", "")
    utm_source = user_data.get("utm_source", "неизвестно")

    total_score = quiz_result.get("total_score", 0)
    profile = quiz_result.get("profile", "")
    main_tag = quiz_result.get("main_tag", "")
    answers = quiz_result.get("answers", {})

    # Format answers
    answer_lines = []
    question_titles = [
        "Умственная усталость",
        "Принятие решений",
        "Память",
        "Концентрация",
        "Сон",
        "Многозадачность",
        "Интерес"
    ]

    for i in range(1, 8):
        q_key = f'q{i}'
        if q_key in answers:
            answer_label = answers[q_key].get('label', 'н/д')
            answer_lines.append(f"{i}. {question_titles[i-1]} → {answer_label}")

    answers_text = "\n".join(answer_lines)

    card = f"""📋 <b>НОВЫЙ ЛИД</b>

👤 <b>Имя:</b> {first_name} {last_name}
📱 <b>Username:</b> @{username if username else 'отсутствует'}
🆔 <b>User ID:</b> <code>{user_id}</code>
📊 <b>Источник:</b> {utm_source}

━━━ <b>РЕЗУЛЬТАТЫ КВИЗА</b> ━━━
📈 <b>Балл:</b> {total_score}/24
🏷 <b>Профиль:</b> {profile}
🎯 <b>Приоритет:</b> {TAG_LABELS.get(main_tag, main_tag)}

━━━ <b>ОТВЕТЫ</b> ━━━
{answers_text}

📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}
🔗 Чтобы ответить — просто напишите в этот топик"""

    return card
