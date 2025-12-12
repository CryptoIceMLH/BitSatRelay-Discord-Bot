import asyncio
import json
import time
import httpx
from websockets import connect

from .crud import get_settings

# Gateway connection
gateway_ws = None
heartbeat_interval = None
session_id = None
sequence = None

async def wait_for_discord_updates():
    """Main background task - runs continuously"""
    global gateway_ws, session_id, sequence

    while True:
        try:
            settings = await get_settings()

            if not settings or not settings.get('enabled') or not settings.get('bot_token'):
                await asyncio.sleep(30)
                continue

            # Connect to Discord Gateway if not connected
            if gateway_ws is None or gateway_ws.closed:
                await connect_to_gateway(settings['bot_token'])

            # Update status
            await update_discord_status(settings)

            # Sleep based on rotation speed
            await asyncio.sleep(settings['rotation_speed'])

        except Exception as e:
            print(f"Discord bot error: {e}")
            gateway_ws = None  # Reset connection on error
            await asyncio.sleep(30)

async def connect_to_gateway(bot_token):
    """Connect to Discord Gateway WebSocket"""
    global gateway_ws, heartbeat_interval, session_id, sequence

    try:
        # Connect to Gateway
        gateway_ws = await connect("wss://gateway.discord.gg/?v=10&encoding=json")

        # Receive Hello event (OP 10)
        hello = json.loads(await gateway_ws.recv())
        heartbeat_interval = hello['d']['heartbeat_interval'] / 1000  # Convert to seconds

        # Start heartbeat task
        asyncio.create_task(send_heartbeat())

        # Send Identify payload (OP 2)
        identify = {
            "op": 2,
            "d": {
                "token": bot_token,
                "intents": 0,  # No intents needed for just updating presence
                "properties": {
                    "os": "linux",
                    "browser": "lnbits",
                    "device": "lnbits"
                },
                "presence": {
                    "status": "online",
                    "afk": False
                }
            }
        }
        await gateway_ws.send(json.dumps(identify))

        # Receive Ready event (OP 0)
        ready = json.loads(await gateway_ws.recv())
        if ready['op'] == 0 and ready['t'] == 'READY':
            session_id = ready['d']['session_id']
            print(f"Discord bot connected: {ready['d']['user']['username']}#{ready['d']['user']['discriminator']}")

        # Start listening for events
        asyncio.create_task(listen_for_events())

    except Exception as e:
        print(f"Gateway connection error: {e}")
        gateway_ws = None

async def send_heartbeat():
    """Send heartbeat to keep connection alive"""
    global gateway_ws, heartbeat_interval, sequence

    while gateway_ws and not gateway_ws.closed:
        try:
            await asyncio.sleep(heartbeat_interval)
            heartbeat = {"op": 1, "d": sequence}
            await gateway_ws.send(json.dumps(heartbeat))
        except Exception as e:
            print(f"Heartbeat error: {e}")
            break

async def listen_for_events():
    """Listen for Gateway events and update sequence number"""
    global gateway_ws, sequence

    try:
        async for message in gateway_ws:
            data = json.loads(message)

            # Update sequence number
            if data.get('s'):
                sequence = data['s']

            # Handle reconnect request (OP 7)
            if data['op'] == 7:
                print("Discord requested reconnect")
                gateway_ws = None
                break
    except Exception as e:
        print(f"Event listener error: {e}")
        gateway_ws = None

async def update_discord_status(settings):
    """Fetch stats and update Discord bot status"""
    global gateway_ws

    if gateway_ws is None or gateway_ws.closed:
        return

    # Fetch stats from BitSatCredit API using httpx
    async with httpx.AsyncClient() as client:
        try:
            stats_response = await client.get(
                f"{settings['lnbits_api_url']}/bitsatcredit/api/v1/stats",
                timeout=5.0
            )
            stats = stats_response.json()

            status_response = await client.get(
                f"{settings['lnbits_api_url']}/bitsatcredit/api/v1/system/status",
                timeout=5.0
            )
            status_data = status_response.json()

            price_response = await client.get(
                f"{settings['lnbits_api_url']}/bitsatcredit/api/v1/settings/price",
                timeout=5.0
            )
            price_data = price_response.json()
            price_per_msg = price_data.get('price', 0)

        except Exception as e:
            print(f"Error fetching stats: {e}")
            return

    # Build list of all statuses (4 default + custom announcements)
    statuses = []

    # Default statuses
    statuses.append(('custom', f"📊 {stats['total_users']:,} users | {stats['total_messages']:,} messages"))
    statuses.append(('watching', 'satellite network'))
    statuses.append(('custom', f"⚡ {price_per_msg} sats per message"))

    # System online/offline status
    if status_data.get('is_online', False):
        statuses.append(('custom', "🟢 System: Online"))
    else:
        statuses.append(('custom', "🔴 System: Offline"))

    # Add custom announcements
    announcements = settings.get('announcements', [])
    if announcements and isinstance(announcements, list):
        for announcement in announcements:
            if announcement.strip():
                statuses.append(('custom', announcement.strip()))

    # Rotate through all statuses
    if len(statuses) == 0:
        return

    cycle = int(time.time() / settings['rotation_speed']) % len(statuses)
    activity_type, activity_name = statuses[cycle]

    # Build presence update payload (OP 3)
    # Activity types: 0=Game, 1=Streaming, 2=Listening, 3=Watching, 4=Custom
    if activity_type == 'custom':
        activities = [{
            "type": 4,  # Custom status
            "name": "Custom Status",
            "state": activity_name
        }]
    elif activity_type == 'watching':
        activities = [{
            "type": 3,  # Watching
            "name": activity_name
        }]
    else:
        activities = [{
            "type": 0,  # Playing
            "name": activity_name
        }]

    presence_update = {
        "op": 3,
        "d": {
            "since": None,
            "activities": activities,
            "status": "online",
            "afk": False
        }
    }

    try:
        await gateway_ws.send(json.dumps(presence_update))
    except Exception as e:
        print(f"Error updating presence: {e}")
        gateway_ws = None
