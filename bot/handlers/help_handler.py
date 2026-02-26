"""Help command handler"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils.formatting import format_help_message

router = Router()


@router.message(Command("help"))
@router.message(F.text == "❓ Помощь")
async def cmd_help(message: Message):
    """Handle /help command"""
    await message.answer(
        format_help_message(),
        parse_mode="HTML"
    )
