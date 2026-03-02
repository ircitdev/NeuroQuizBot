"""Forum topic management for CRM supergroup"""
from typing import Dict, Any
from datetime import datetime
from aiogram import Bot
from bot.config import SUPERGROUP_CHAT_ID
from bot.services.quiz_data import TAG_LABELS


async def create_lead_topic(bot: Bot, user_data: Dict[str, Any], quiz_result: Dict[str, Any]) -> int:
    """
    Create a forum topic in supergroup for the lead

    If user already has a thread_id, returns existing thread_id instead of creating new one.

    Args:
        bot: Bot instance
        user_data: User data dict
        quiz_result: Quiz result dict

    Returns:
        thread_id: Forum thread ID
    """
    # Check if user already has a topic
    existing_thread_id = user_data.get("thread_id")
    if existing_thread_id:
        print(f"User {user_data.get('tg_user_id')} already has topic {existing_thread_id}, skipping creation")
        return existing_thread_id

    # Create topic name
    name = user_data.get("first_name", "Аноним")
    username = user_data.get("username", "")
    topic_name = f"🧠 {name}"
    if username:
        topic_name += f" (@{username})"

    # Truncate to 128 chars (Telegram limit)
    topic_name = topic_name[:128]

    # Create forum topic
    print(f"[TOPIC] Creating forum topic: {topic_name} in chat {SUPERGROUP_CHAT_ID}")
    try:
        result = await bot.create_forum_topic(
            chat_id=SUPERGROUP_CHAT_ID,
            name=topic_name
        )
        print(f"[TOPIC] Forum topic created successfully")
    except Exception as e:
        print(f"[TOPIC] Error creating forum topic: {e}")
        raise

    thread_id = result.message_thread_id
    print(f"[TOPIC] Thread ID: {thread_id}")

    # Send lead card to topic
    card = format_lead_card(user_data, quiz_result)
    print(f"[TOPIC] Sending lead card to thread {thread_id}...")
    try:
        await bot.send_message(
            chat_id=SUPERGROUP_CHAT_ID,
            message_thread_id=thread_id,
            text=card,
            parse_mode="HTML"
        )
        print(f"[TOPIC] Lead card sent successfully")
    except Exception as e:
        print(f"[TOPIC] Error sending lead card: {e}")
        raise

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
