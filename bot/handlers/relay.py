"""Message relay system for bidirectional messaging"""
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.config import SUPERGROUP_CHAT_ID
from bot.db import db
from bot.handlers.quiz import QuizStates

router = Router()


@router.message(F.chat.id == SUPERGROUP_CHAT_ID)
async def manager_to_user(message: Message):
    """
    Relay message from manager (in forum topic) to user

    Manager writes in topic → Bot forwards to user's private chat
    """
    # Ignore messages from bot itself
    if message.from_user.is_bot:
        return

    # Check if message is in a thread
    if not message.message_thread_id:
        return

    # Get user by thread_id
    user = await db.get_user_by_thread(message.message_thread_id)
    if not user:
        # Thread doesn't belong to any user
        return

    # Log message
    await db.log_message(
        user_id=user['tg_user_id'],
        direction='out',
        text=message.text or message.caption,
        tg_message_id=message.message_id
    )

    # Forward message to user
    try:
        await message.copy_to(
            chat_id=user['tg_user_id']
        )
    except Exception as e:
        # User might have blocked the bot
        print(f"Error forwarding message to user {user['tg_user_id']}: {e}")
        await message.reply(
            "⚠️ Не удалось отправить сообщение пользователю. "
            "Возможно, он заблокировал бота."
        )


@router.message(F.chat.type == "private")
async def user_to_manager(message: Message, state: FSMContext):
    """
    Relay message from user to manager (forum topic)

    User writes to bot → Bot forwards to their topic in supergroup
    """
    # Don't relay during active quiz (but allow after completion)
    current_state = await state.get_state()
    if current_state and current_state.startswith("QuizStates:") and not current_state.endswith(":completed"):
        # User is actively taking quiz, don't relay
        return

    # Get user data
    user = await db.get_user(message.from_user.id)
    if not user or not user.get('thread_id'):
        # User doesn't have a thread yet (hasn't completed quiz)
        await message.answer(
            "Для начала работы пройдите квиз: /quiz\n\n"
            "После этого вы сможете общаться с нашими менеджерами."
        )
        return

    # Log message
    await db.log_message(
        user_id=message.from_user.id,
        direction='in',
        text=message.text or message.caption,
        tg_message_id=message.message_id
    )

    # Forward message to supergroup topic
    try:
        await message.copy_to(
            chat_id=SUPERGROUP_CHAT_ID,
            message_thread_id=user['thread_id']
        )
    except Exception as e:
        print(f"Error forwarding message to supergroup: {e}")
        await message.answer(
            "⚠️ Произошла ошибка при отправке сообщения. "
            "Попробуйте позже или свяжитесь с поддержкой."
        )
