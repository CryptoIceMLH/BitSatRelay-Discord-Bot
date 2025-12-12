import asyncio
import requests
import time

from .crud import get_settings

# Discord bot - initialized lazily
bot = None

async def wait_for_discord_updates():
    """Main background task - runs continuously"""
    global bot

    while True:
        try:
            settings = await get_settings()

            if not settings or not settings.get('enabled') or not settings.get('bot_token'):
                await asyncio.sleep(30)
                continue

            # Lazy import discord.py (only when actually needed)
            if bot is None:
                try:
                    import discord
                    intents = discord.Intents.default()
                    bot = discord.Client(intents=intents)

                    @bot.event
                    async def on_ready():
                        print(f"Discord bot logged in as {bot.user}")

                except ImportError:
                    print("discord.py not installed. Install with: pip install discord.py>=2.0.0")
                    await asyncio.sleep(300)  # Wait 5 minutes before retrying
                    continue

            # Start Discord bot if not running
            if not bot.is_ready():
                await bot.start(settings['bot_token'])

            # Update status
            await update_discord_status(settings)

            # Sleep based on rotation speed
            await asyncio.sleep(settings['rotation_speed'])

        except Exception as e:
            print(f"Discord bot error: {e}")
            await asyncio.sleep(30)

async def update_discord_status(settings):
    """Fetch stats and update Discord bot status"""

    # Fetch stats from BitSatCredit API
    try:
        stats_response = requests.get(
            f"{settings['lnbits_api_url']}/bitsatcredit/api/v1/stats",
            timeout=5
        )
        stats = stats_response.json()

        status_response = requests.get(
            f"{settings['lnbits_api_url']}/bitsatcredit/api/v1/system/status",
            timeout=5
        )
        status = status_response.json()

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return

    # Fetch price per message
    try:
        price_response = requests.get(
            f"{settings['lnbits_api_url']}/bitsatcredit/api/v1/settings/price",
            timeout=5
        )
        price_data = price_response.json()
        price_per_msg = price_data.get('price', 0)
    except:
        price_per_msg = 0

    # Import discord for activity types
    import discord

    # Build list of all statuses (4 default + custom announcements)
    statuses = []

    # Default statuses
    statuses.append(('stats', stats, None))  # User/message stats
    statuses.append(('watching', None, None))  # Watching satellite network
    statuses.append(('price', price_per_msg, None))  # Price per message

    # System online/offline status
    if status.get('is_online', False):
        statuses.append(('online', None, None))
    else:
        statuses.append(('offline', None, None))

    # Add custom announcements
    announcements = settings.get('announcements', [])
    if announcements and isinstance(announcements, list):
        for announcement in announcements:
            if announcement.strip():
                statuses.append(('custom', None, announcement.strip()))

    # Rotate through all statuses
    if len(statuses) == 0:
        return

    cycle = int(time.time() / settings['rotation_speed']) % len(statuses)
    status_type, data, text = statuses[cycle]

    # Create activity based on type
    if status_type == 'stats':
        activity = discord.CustomActivity(
            name=f"📊 {data['total_users']:,} users | {data['total_messages']:,} messages"
        )
    elif status_type == 'watching':
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="satellite network"
        )
    elif status_type == 'price':
        activity = discord.CustomActivity(
            name=f"⚡ {data} sats per message"
        )
    elif status_type == 'online':
        activity = discord.CustomActivity(name="🟢 System: Online")
    elif status_type == 'offline':
        activity = discord.CustomActivity(name="🔴 System: Offline")
    elif status_type == 'custom':
        activity = discord.CustomActivity(name=text)

    await bot.change_presence(activity=activity)
