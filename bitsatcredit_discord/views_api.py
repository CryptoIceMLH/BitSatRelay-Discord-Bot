from fastapi import APIRouter, Depends
from lnbits.core.models import User
from lnbits.decorators import check_admin

from .crud import get_settings, update_settings

# API routes
bitsatcredit_discord_api_router: APIRouter = APIRouter()

@bitsatcredit_discord_api_router.get("/api/v1/settings")
async def api_get_settings(user: User = Depends(check_admin)):
    """Get current Discord bot settings"""
    settings = await get_settings()
    return settings or {}

@bitsatcredit_discord_api_router.post("/api/v1/settings")
async def api_update_settings(data: dict, user: User = Depends(check_admin)):
    """Update Discord bot settings"""
    await update_settings(data)
    return {"success": True}

@bitsatcredit_discord_api_router.get("/api/v1/status")
async def api_status():
    """Health check endpoint"""
    return {"status": "ok", "extension": "bitsatcredit_discord"}
