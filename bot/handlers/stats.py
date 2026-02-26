"""Statistics handler for admins"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import ADMIN_IDS
from bot.db import db

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Show bot statistics (admin only)"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Эта команда доступна только администраторам.")
        return

    stats = await db.get_stats()

    # Format statistics
    profiles_text = "\n".join([
        f"  • {profile}: {count}"
        for profile, count in stats.get('profiles', {}).items()
    ])

    utm_text = "\n".join([
        f"  • {source}: {count}"
        for source, count in stats.get('utm_sources', {}).items()
    ])

    text = f"""📊 <b>Статистика бота</b>

👥 <b>Всего пользователей:</b> {stats.get('total_users', 0)}
✅ <b>Прошли квиз:</b> {stats.get('completed_quiz', 0)}
❌ <b>Не прошли:</b> {stats.get('total_users', 0) - stats.get('completed_quiz', 0)}

📈 <b>Средний балл:</b> {stats.get('average_score', 0):.1f}/24

<b>Распределение по профилям:</b>
{profiles_text or '  Нет данных'}

<b>Источники трафика:</b>
{utm_text or '  Нет данных'}"""

    await message.answer(text, parse_mode="HTML")
