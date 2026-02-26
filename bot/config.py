"""Configuration settings for the bot"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPERGROUP_CHAT_ID = int(os.getenv("SUPERGROUP_CHAT_ID", "-1003596687347"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/bot.db")

# Admin settings
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: List[int] = [int(x.strip()) for x in ADMIN_IDS_STR.split(",") if x.strip()]

# Validate required settings
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required in .env file")

# Database file path for SQLite
DB_PATH = DATABASE_URL.replace("sqlite:///", "")

# Event settings
EVENT_NAME = "Всемогущие Нейроны 3"
EVENT_DATE = "20 марта 2026"
EVENT_VENUE = "Крокус-Экспо"
