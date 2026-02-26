"""Main bot entry point"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN
from bot.db import db
from bot.handlers import main_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """Execute on bot startup"""
    logger.info("Initializing database...")
    await db.init_db()
    logger.info("Database initialized")

    # Set bot commands for regular users
    from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
    from bot.config import ADMIN_IDS

    # Commands for all users
    default_commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="quiz", description="Пройти квиз по нейрофизиологии"),
        BotCommand(command="result", description="Показать мой результат"),
        BotCommand(command="help", description="Справка и помощь"),
    ]

    await bot.set_my_commands(default_commands, scope=BotCommandScopeDefault())

    # Commands for admins (with /stats)
    admin_commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="quiz", description="Пройти квиз по нейрофизиологии"),
        BotCommand(command="result", description="Показать мой результат"),
        BotCommand(command="help", description="Справка и помощь"),
        BotCommand(command="stats", description="📊 Статистика бота (только для админов)"),
    ]

    # Set admin commands for each admin
    for admin_id in ADMIN_IDS:
        try:
            await bot.set_my_commands(
                admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
        except Exception as e:
            logger.warning(f"Could not set commands for admin {admin_id}: {e}")

    bot_info = await bot.get_me()
    logger.info(f"Bot started: @{bot_info.username}")
    logger.info(f"Commands set for {len(ADMIN_IDS)} admin(s)")


async def on_shutdown(bot: Bot):
    """Execute on bot shutdown"""
    logger.info("Bot shutting down...")
    await bot.session.close()


async def main():
    """Main function"""
    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register routers
    dp.include_router(main_router)

    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Start polling
    logger.info("Starting polling...")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    except Exception as e:
        logger.error(f"Error during polling: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
