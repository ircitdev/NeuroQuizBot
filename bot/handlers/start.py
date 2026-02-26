"""Start command handler"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.db import db
from bot.keyboards.quiz_kb import get_start_quiz_keyboard
from bot.utils.formatting import format_welcome_message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command with optional deep link"""
    # Clear any existing state
    await state.clear()

    # Extract UTM source from deep link
    args = message.text.split(maxsplit=1)
    utm_source = None
    if len(args) > 1:
        # /start lead_site or /start lead_instagram
        utm_source = args[1]

    # Save or update user
    await db.add_user(
        tg_user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        utm_source=utm_source
    )

    # Send welcome message
    welcome_text = format_welcome_message(message.from_user.first_name or "друг")
    await message.answer(
        welcome_text,
        reply_markup=get_start_quiz_keyboard()
    )
