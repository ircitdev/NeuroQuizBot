"""Broadcast handler for mass messaging"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import ADMIN_IDS
from bot.db import db

router = Router()


class BroadcastStates(StatesGroup):
    """Broadcast FSM states"""
    waiting_message = State()


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, state: FSMContext):
    """Start broadcast process (admin only)"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Эта команда доступна только администраторам.")
        return

    await state.set_state(BroadcastStates.waiting_message)
    await message.answer(
        "📢 <b>Режим массовой рассылки</b>\n\n"
        "Отправьте сообщение, которое хотите разослать всем пользователям.\n"
        "Поддерживаются: текст, фото, видео, документы.\n\n"
        "Для отмены отправьте /cancel",
        parse_mode="HTML"
    )


@router.message(Command("cancel"), BroadcastStates.waiting_message)
async def cancel_broadcast(message: Message, state: FSMContext):
    """Cancel broadcast"""
    await state.clear()
    await message.answer("❌ Рассылка отменена.")


@router.message(BroadcastStates.waiting_message)
async def process_broadcast(message: Message, state: FSMContext):
    """Process and send broadcast message"""
    await state.clear()

    # Get all users
    async with db._Database__get_connection() as conn:
        conn.row_factory = db.aiosqlite.Row
        async with conn.execute("SELECT DISTINCT tg_user_id FROM users") as cursor:
            users = await cursor.fetchall()

    if not users:
        await message.answer("⚠️ Нет пользователей для рассылки.")
        return

    total_users = len(users)

    # Confirm broadcast
    await message.answer(
        f"📊 Начинаю рассылку для {total_users} пользователей...\n"
        f"⏳ Это может занять некоторое время."
    )

    # Send to all users
    success_count = 0
    failed_count = 0
    blocked_count = 0

    for user_row in users:
        user_id = user_row['tg_user_id']

        # Skip sending to self
        if user_id == message.from_user.id:
            continue

        try:
            # Copy message to user
            await message.copy_to(chat_id=user_id)
            success_count += 1

            # Small delay to avoid rate limits
            import asyncio
            await asyncio.sleep(0.05)  # 50ms delay between messages

        except Exception as e:
            error_text = str(e).lower()
            if 'blocked' in error_text or 'user is deactivated' in error_text:
                blocked_count += 1
            else:
                failed_count += 1

    # Report results
    result_text = f"""✅ <b>Рассылка завершена</b>

📊 Статистика:
• Всего пользователей: {total_users}
• Успешно отправлено: {success_count}
• Заблокировали бота: {blocked_count}
• Ошибки отправки: {failed_count}"""

    await message.answer(result_text, parse_mode="HTML")


# Helper method to add to Database class
async def _Database__get_connection(self):
    """Get database connection (helper for broadcast)"""
    import aiosqlite
    return await aiosqlite.connect(self.db_path)

# Patch the Database class
db._Database__get_connection = _Database__get_connection.__get__(db, type(db))
