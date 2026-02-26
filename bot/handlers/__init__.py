"""Handlers module"""
from aiogram import Router
from . import start, quiz, relay, help_handler, stats

# Create main router
main_router = Router()

# Include all handler routers
main_router.include_router(start.router)
main_router.include_router(quiz.router)
main_router.include_router(help_handler.router)
main_router.include_router(stats.router)
main_router.include_router(relay.router)  # Relay should be last to catch remaining messages
