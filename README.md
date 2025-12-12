# BitSatRelay Discord Bot - LNbits Extension

Display your BitSatRelay network statistics in Discord as a rotating bot status.

## Overview

This LNbits extension creates a Discord bot that monitors your BitSatCredit extension and displays live network statistics as rotating status messages visible in your Discord server's member list.

### Features

- 🤖 **Auto-updating Discord bot status**
- 📊 **4 rotating status displays:**
  - User count and message count
  - Satellite network monitoring indicator
  - Current price per message
  - System online/offline status (with color indicators)
- 🎛️ **Web-based admin interface** integrated into LNbits
- ⚙️ **Configurable rotation speed**
- 🔗 **Clickable link in bot profile** to your credit top-up page
- 🛡️ **Zero risk to existing BitSatCredit extension** (queries public APIs only)

## What You'll See in Discord

```
🤖 BitSatRelay Monitor [BOT]
   📊 150 users | 12,500 messages

(30 seconds later...)
   🛰️ Watching satellite network

(30 seconds later...)
   ⚡ 10 sats per message

(30 seconds later...)
   🟢 System: Online  (or 🔴 System: Offline)
```

## Prerequisites

- LNbits instance with BitSatCredit extension installed
- Discord account
- Discord server where you have admin permissions

## Installation

### Step 1: Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name it: **"BitSatRelay Monitor"** (or your preferred name)
4. Go to **"Bot"** tab → Click **"Add Bot"**
5. Under **"Privileged Gateway Intents"**:
   - ✅ Enable **"Presence Intent"** (required)
   - ✅ Enable **"Server Members Intent"** (optional)
6. Click **"Reset Token"** → **Copy the bot token** (save it securely!)

### Step 2: Add Clickable Link to Bot Profile

7. Still in Developer Portal → Go to **"General Information"** tab
8. Scroll down to **"LINKS"** section
9. Click **"Add Link"**
10. **Label**: `Top Up Credits`
11. **URL**: `
12. **Save changes**

### Step 3: Invite Bot to Your Server

13. Go to **"OAuth2"** → **"URL Generator"**
14. Under **"Scopes"**, select: ✅ `bot`
15. **No permissions needed** (bot only updates its own status)
16. **Copy the generated URL** at the bottom
17. Paste URL in browser → Select your server → **Authorize**

Your bot will appear offline until the extension is configured!

### Step 4: Install Extension in LNbits

#### Option A: Manual Installation (Development)

```bash
# Copy extension folder to LNbits extensions directory
cp -r bitsatcredit_discord /path/to/lnbits/lnbits/extensions/

# Install dependencies
pip install -r requirements.txt

# Restart LNbits
systemctl restart lnbits
```

#### Option B: From GitHub Repository (Production)

```bash
# Clone repository
cd /path/to/lnbits/lnbits/extensions/
git clone https://github.com/yourusername/BitSatRelay-Discord-Bot.git
ln -s BitSatRelay-Discord-Bot/bitsatcredit_discord bitsatcredit_discord

# Install dependencies
pip install -r BitSatRelay-Discord-Bot/requirements.txt

# Restart LNbits
systemctl restart lnbits
```

### Step 5: Configure Extension

1. Open **LNbits admin** interface
2. Go to **"Extensions"** → Find **"BitSatCredit Discord"**
3. Click to open the extension page
4. **Paste your Discord bot token** from Step 1
5. Set **rotation speed** (default: 30 seconds)
6. Verify **API URL**: `
7. Toggle **"Bot Enabled"** to ON
8. Click **"Save Settings"**

**Your bot should now appear online in Discord!** 🎉

## Configuration

### Settings

- **Bot Token**: Discord bot token from Developer Portal (required)
- **Rotation Speed**: How often to change the displayed stat (in seconds, default: 30)
- **LNbits API URL**: Base URL for BitSatCredit API 
- **Enabled**: Toggle bot on/off

### Status Rotation

The bot cycles through 4 status displays:

1. **📊 Stats Summary**: `150 users | 12,500 messages`
2. **🛰️ Monitoring**: `Watching satellite network`
3. **⚡ Pricing**: `10 sats per message` (live from API)
4. **🟢/🔴 System Status**: `System: Online` or `System: Offline`

## API Endpoints

This extension queries the following **public** BitSatCredit API endpoints:

- `GET /bitsatcredit/api/v1/stats` - Network statistics
- `GET /bitsatcredit/api/v1/system/status` - System online/offline status
- `GET /bitsatcredit/api/v1/settings/price` - Current price per message

**No modifications to the BitSatCredit extension are required!**

## Troubleshooting

### Bot appears offline

- Verify bot token is correct
- Check that "Bot Enabled" is toggled ON
- Verify Presence Intent is enabled in Discord Developer Portal
- Check LNbits logs for errors: `journalctl -u lnbits -f`

### Status not updating

- Verify API URL is correct
- Check that BitSatCredit extension is running
- Try reducing rotation speed to test faster
- Check browser console for JavaScript errors

### Bot can't connect to Discord

- Verify bot token hasn't been regenerated
- Check internet connectivity from server
- Ensure discord.py library is installed: `pip install discord.py>=2.0.0`

## Development

### Project Structure

```
bitsatcredit_discord/
├── __init__.py          # Extension initialization
├── config.py            # Extension metadata
├── views.py             # API routes and admin page
├── tasks.py             # Discord bot background task
├── crud.py              # Database operations
├── models.py            # Data models
├── migrations.py        # Database schema
├── templates/
│   └── bitsatcredit_discord/
│       └── index.html   # Admin UI
└── static/
    └── js/
        └── index.js     # Frontend JavaScript (optional)
```

### Database Schema

**Table**: `discord_settings`

| Column           | Type      | Description                          |
|------------------|-----------|--------------------------------------|
| id               | INTEGER   | Primary key                          |
| bot_token        | TEXT      | Discord bot token                    |
| enabled          | BOOLEAN   | Bot enabled/disabled                 |
| rotation_speed   | INTEGER   | Seconds between status changes       |
| lnbits_api_url   | TEXT      | BitSatCredit API base URL            |
| created_at       | TIMESTAMP | Record creation time                 |
| updated_at       | TIMESTAMP | Last update time                     |

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file

## Support

- **Issues**: https://github.com/yourusername/BitSatRelay-Discord-Bot/issues
- **Website**: https://www.molonlabe.holdings
-

## Credits

Built for the BitSatRelay project by the BitSatRelay team.

- **BitSatCredit Extension**: Payment system for satellite messages
- **BitSatRelay**: Nostr to satellite bridge
- **LNbits**: Bitcoin Lightning Network wallet and tools

---

**🛰️ Powered by Bitcoin Lightning Network**
