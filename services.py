"""Business logic for Discord bot integration"""
import requests
from typing import Dict, Any, Optional

async def fetch_bitsatcredit_stats(api_url: str) -> Optional[Dict[str, Any]]:
    """Fetch network statistics from BitSatCredit API"""
    try:
        response = requests.get(
            f"{api_url}/bitsatcredit/api/v1/stats",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None

async def fetch_system_status(api_url: str) -> Optional[Dict[str, Any]]:
    """Fetch system status from BitSatCredit API"""
    try:
        response = requests.get(
            f"{api_url}/bitsatcredit/api/v1/system/status",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching status: {e}")
        return None

async def fetch_price_per_message(api_url: str) -> Optional[int]:
    """Fetch current price per message from BitSatCredit API"""
    try:
        response = requests.get(
            f"{api_url}/bitsatcredit/api/v1/settings/price",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return data.get('price', 0)
    except Exception as e:
        print(f"Error fetching price: {e}")
        return 0
