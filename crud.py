import json
from datetime import datetime
from lnbits.db import Database

db = Database("ext_bitsatcredit_discord")

async def get_settings():
    """Get Discord bot settings from database"""
    row = await db.fetchone("SELECT * FROM discord_settings LIMIT 1")
    if row:
        settings = dict(row)
        # Parse announcements JSON string to array
        if 'announcements' in settings and settings['announcements']:
            try:
                settings['announcements'] = json.loads(settings['announcements'])
            except:
                settings['announcements'] = []
        else:
            settings['announcements'] = []
        return settings
    return None

async def update_settings(data: dict):
    """Update or create settings"""
    existing = await get_settings()

    # Convert announcements array to JSON string
    announcements = data.get("announcements", [])
    if isinstance(announcements, list):
        announcements_json = json.dumps(announcements)
    else:
        announcements_json = "[]"

    if existing:
        await db.execute(
            """
            UPDATE discord_settings
            SET bot_token = :bot_token, enabled = :enabled, rotation_speed = :rotation_speed,
                lnbits_api_url = :lnbits_api_url, announcements = :announcements, updated_at = :updated_at
            WHERE id = :id
            """,
            {
                "bot_token": data.get("bot_token"),
                "enabled": data.get("enabled", True),
                "rotation_speed": data.get("rotation_speed", 30),
                "lnbits_api_url": data.get("lnbits_api_url", "https://lnbits.molonlabe.holdings"),
                "announcements": announcements_json,
                "updated_at": datetime.now(),
                "id": existing["id"]
            }
        )
    else:
        await db.execute(
            """
            INSERT INTO discord_settings (bot_token, enabled, rotation_speed, lnbits_api_url, announcements, created_at, updated_at)
            VALUES (:bot_token, :enabled, :rotation_speed, :lnbits_api_url, :announcements, :created_at, :updated_at)
            """,
            {
                "bot_token": data.get("bot_token"),
                "enabled": data.get("enabled", True),
                "rotation_speed": data.get("rotation_speed", 30),
                "lnbits_api_url": data.get("lnbits_api_url", "https://lnbits.molonlabe.holdings"),
                "announcements": announcements_json,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        )
