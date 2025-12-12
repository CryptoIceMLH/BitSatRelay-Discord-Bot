async def m001_initial(db):
    """
    Initial database schema for Discord bot settings
    """
    await db.execute(
        """
        CREATE TABLE discord_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_token TEXT NOT NULL,
            enabled BOOLEAN DEFAULT 1,
            rotation_speed INTEGER DEFAULT 30,
            lnbits_api_url TEXT DEFAULT 'https://lnbits.molonlabe.holdings',
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

async def m002_add_announcements(db):
    """
    Add announcements field for custom scrolling messages
    """
    await db.execute(
        """
        ALTER TABLE discord_settings
        ADD COLUMN announcements TEXT DEFAULT '[]'
        """
    )
