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

            if not settings or not settings.enabled or not settings.bot_token:
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
                await bot.start(settings.bot_token)

            # Update status
            await update_discord_status(settings)

            # Sleep based on rotation speed
            await asyncio.sleep(settings.rotation_speed)

        except Exception as e:
            print(f"Discord bot error: {e}")
            await asyncio.sleep(30)

async def update_discord_status(settings):
    """Fetch stats and update Discord bot status"""

    # Fetch stats from BitSatCredit API
    try:
        stats_response = requests.get(
            f"{settings.lnbits_api_url}/bitsatcredit/api/v1/stats",
            timeout=5
        )
        stats = stats_response.json()

        status_response = requests.get(
            f"{settings.lnbits_api_url}/bitsatcredit/api/v1/system/status",
            timeout=5
        )
        status = status_response.json()

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return

    # Fetch price per message
    try:
        price_response = requests.get(
            f"{settings.lnbits_api_url}/bitsatcredit/api/v1/settings/price",
            timeout=5
        )
        price_data = price_response.json()
        price_per_msg = price_data.get('price', 0)
    except:
        price_per_msg = 0

    # Import discord for activity types
    import discord

    # Determine which status to show (rotate through 4 options)
    cycle = int(time.time() / settings.rotation_speed) % 4

    if cycle == 0:
        # Cycle 1: X users | Y messages
        activity = discord.CustomActivity(
            name=f"📊 {stats['total_users']:,} users | {stats['total_messages']:,} messages"
        )
    elif cycle == 1:
        # Cycle 2: Watching satellite network
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="satellite network"
        )
    elif cycle == 2:
        # Cycle 3: Price per message
        activity = discord.CustomActivity(
            name=f"⚡ {price_per_msg} sats per message"
        )
    else:
        # Cycle 4: Status with emoji based on system status
        if status.get('is_online', False):
            status_text = "🟢 System: Online"
        else:
            status_text = "🔴 System: Offline"

        activity = discord.CustomActivity(name=status_text)

    await bot.change_presence(activity=activity)
