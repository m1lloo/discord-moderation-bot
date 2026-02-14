import aiosqlite
import os
from datetime import datetime
from utils.config import DATABASE_PATH
from utils.logger import get_logger

logger = get_logger()

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cases (
                    case_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    target_user_id INTEGER NOT NULL,
                    moderator_user_id INTEGER NOT NULL,
                    reason TEXT,
                    duration_seconds INTEGER,
                    created_at TEXT NOT NULL
                )
            """)
            await db.commit()
            logger.info("Database initialized")
    
    async def create_case(self, guild_id, action, target_user_id, moderator_user_id, reason=None, duration_seconds=None):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO cases (guild_id, action, target_user_id, moderator_user_id, reason, duration_seconds, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (guild_id, action, target_user_id, moderator_user_id, reason, duration_seconds, datetime.utcnow().isoformat()))
            await db.commit()
            return cursor.lastrowid
    
    async def get_cases(self, guild_id, target_user_id=None):
        async with aiosqlite.connect(self.db_path) as db:
            if target_user_id:
                cursor = await db.execute("""
                    SELECT * FROM cases WHERE guild_id = ? AND target_user_id = ? ORDER BY created_at DESC
                """, (guild_id, target_user_id))
            else:
                cursor = await db.execute("""
                    SELECT * FROM cases WHERE guild_id = ? ORDER BY created_at DESC
                """, (guild_id,))
            return await cursor.fetchall()
    
    async def clear_cases(self, guild_id, target_user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                DELETE FROM cases WHERE guild_id = ? AND target_user_id = ?
            """, (guild_id, target_user_id))
            await db.commit()
            return True

db = Database()
