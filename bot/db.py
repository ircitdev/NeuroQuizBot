"""Database setup and operations"""
import aiosqlite
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import json
from bot.config import DB_PATH


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        # Ensure data directory exists
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    async def init_db(self):
        """Initialize database with required tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_user_id BIGINT UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    utm_source TEXT,
                    thread_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Quiz results table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id BIGINT NOT NULL,
                    answers TEXT NOT NULL,
                    total_score INTEGER NOT NULL,
                    profile TEXT NOT NULL,
                    main_tag TEXT NOT NULL,
                    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (tg_user_id)
                )
            """)

            # Messages table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id BIGINT NOT NULL,
                    direction TEXT NOT NULL,
                    text TEXT,
                    tg_message_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await db.commit()

    async def add_user(self, tg_user_id: int, username: Optional[str] = None,
                      first_name: Optional[str] = None, last_name: Optional[str] = None,
                      utm_source: Optional[str] = None) -> None:
        """Add or update user"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (tg_user_id, username, first_name, last_name, utm_source)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(tg_user_id) DO UPDATE SET
                    username = excluded.username,
                    first_name = excluded.first_name,
                    last_name = excluded.last_name
            """, (tg_user_id, username, first_name, last_name, utm_source))
            await db.commit()

    async def get_user(self, tg_user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by Telegram ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE tg_user_id = ?", (tg_user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def get_user_by_thread(self, thread_id: int) -> Optional[Dict[str, Any]]:
        """Get user by forum thread ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE thread_id = ?", (thread_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def update_user_thread(self, tg_user_id: int, thread_id: int) -> None:
        """Update user's forum thread ID"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET thread_id = ? WHERE tg_user_id = ?",
                (thread_id, tg_user_id)
            )
            await db.commit()

    async def save_quiz_result(self, user_id: int, answers: Dict[str, Any],
                               total_score: int, profile: str, main_tag: str) -> None:
        """Save quiz result"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO quiz_results (user_id, answers, total_score, profile, main_tag)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, json.dumps(answers, ensure_ascii=False), total_score, profile, main_tag))
            await db.commit()

    async def get_last_quiz_result(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's last quiz result"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM quiz_results
                WHERE user_id = ?
                ORDER BY completed_at DESC
                LIMIT 1
            """, (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    result = dict(row)
                    result['answers'] = json.loads(result['answers'])
                    return result
                return None

    async def log_message(self, user_id: int, direction: str, text: Optional[str],
                         tg_message_id: Optional[int] = None) -> None:
        """Log message"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO messages (user_id, direction, text, tg_message_id)
                VALUES (?, ?, ?, ?)
            """, (user_id, direction, text, tg_message_id))
            await db.commit()

    async def get_stats(self) -> Dict[str, Any]:
        """Get bot statistics"""
        async with aiosqlite.connect(self.db_path) as db:
            stats = {}

            # Total users
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                stats['total_users'] = (await cursor.fetchone())[0]

            # Users who completed quiz
            async with db.execute("SELECT COUNT(DISTINCT user_id) FROM quiz_results") as cursor:
                stats['completed_quiz'] = (await cursor.fetchone())[0]

            # Average score
            async with db.execute("SELECT AVG(total_score) FROM quiz_results") as cursor:
                avg_score = (await cursor.fetchone())[0]
                stats['average_score'] = round(avg_score, 1) if avg_score else 0

            # Profile distribution
            async with db.execute("""
                SELECT profile, COUNT(*) as count
                FROM quiz_results
                GROUP BY profile
            """) as cursor:
                stats['profiles'] = {row[0]: row[1] async for row in cursor}

            # UTM sources
            async with db.execute("""
                SELECT utm_source, COUNT(*) as count
                FROM users
                WHERE utm_source IS NOT NULL
                GROUP BY utm_source
            """) as cursor:
                stats['utm_sources'] = {row[0]: row[1] async for row in cursor}

            return stats


# Global database instance
db = Database()
