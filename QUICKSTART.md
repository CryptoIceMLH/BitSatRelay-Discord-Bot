# Quick Start Guide - BitSatRelay Discord Bot

## Fast Setup (5 minutes)

### 1. Create Discord Bot (2 minutes)

1. Visit: https://discord.com/developers/applications
2. Click "New Application" → Name it "BitSatRelay Monitor"
3. Go to "Bot" → "Add Bot"
4. **Enable these intents:**
   - ✅ Presence Intent
   - ✅ Server Members Intent (optional)
5. Click "Reset Token" → **COPY IT** (you'll need this!)
6. Go to "General Information" → "Links" section
7. Add link:
   - Label: `Top Up Credits`
   - URL: `https://lnbits.molonlabe.holdings/bitsatcredit/6e1faaf6356b43029124fdeb5f93a297`

### 2. Invite Bot to Server (1 minute)

1. Go to "OAuth2" → "URL Generator"
2. Select scope: `bot`
3. Copy URL → Open in browser → Select your server → Authorize

### 3. Install Extension (1 minute)

```bash
# Copy to LNbits extensions folder
cp -r bitsatcredit_discord /path/to/lnbits/lnbits/extensions/

# Install dependencies
pip install discord.py>=2.0.0 requests>=2.28.0

# Restart LNbits
systemctl restart lnbits  # or however you run LNbits
```

### 4. Configure (1 minute)

1. Open LNbits admin
2. Go to "Extensions" → "BitSatCredit Discord"
3. Paste your bot token from step 1.5
4. Toggle "Bot Enabled" ON
5. Click "Save Settings"

**DONE!** Your bot should appear online in Discord! 🎉

## What You'll See

The bot status will rotate every 30 seconds:

```
📊 150 users | 12,500 messages
↓ (30s)
🛰️ Watching satellite network
↓ (30s)
⚡ 10 sats per message
↓ (30s)
🟢 System: Online
```

## Troubleshooting

**Bot offline?**
- Check bot token is correct
- Verify "Presence Intent" is enabled
- Make sure bot is enabled in settings

**Status not changing?**
- Wait 30 seconds (default rotation)
- Check LNbits logs: `journalctl -u lnbits -f`
- Verify BitSatCredit API is accessible

## Need Help?

See full [README.md](README.md) for detailed documentation.

---

**Ready to upload to GitHub?**

```bash
cd "E:\MLH BTC\btcsatcoms\BitSatRelay-Discord-Bot"
git init
git add .
git commit -m "Initial commit: BitSatRelay Discord Bot LNbits Extension"
git remote add origin https://github.com/yourusername/BitSatRelay-Discord-Bot.git
git push -u origin main
```
