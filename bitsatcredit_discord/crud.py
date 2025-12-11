from datetime import datetime
from lnbits.db import Database

db = Database("ext_bitsatcredit_discord")

async def get_settings():
    """Get Discord bot settings from database"""
    row = await db.fetchone("SELECT * FROM discord_settings LIMIT 1")
    return row

async def update_settings(data: dict):
    """Update or create settings"""
    existing = await get_settings()

    if existing:
        await db.execute(
            """
            UPDATE discord_settings
            SET bot_token = ?, enabled = ?, rotation_speed = ?, lnbits_api_url = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                data.get("bot_token"),
                data.get("enabled", True),
                data.get("rotation_speed", 30),
                data.get("lnbits_api_url", "https://lnbits.molonlabe.holdings"),
                datetime.now(),
                existing.id
            )
        )
    else:
        await db.execute(
            """
            INSERT INTO discord_settings (bot_token, enabled, rotation_speed, lnbits_api_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("bot_token"),
                data.get("enabled", True),
                data.get("rotation_speed", 30),
                data.get("lnbits_api_url", "https://lnbits.molonlabe.holdings"),
                datetime.now(),
                datetime.now()
            )
        )
