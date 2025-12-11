from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from lnbits.core.models import User
from lnbits.decorators import check_admin

from .crud import get_settings, update_settings

bitsatcredit_discord_ext: APIRouter = APIRouter(
    prefix="/bitsatcredit_discord",
    tags=["BitSatCredit Discord"]
)

templates = Jinja2Templates(directory="templates")

@bitsatcredit_discord_ext.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_admin)):
    """Admin page - Discord bot settings"""
    return templates.TemplateResponse(
        "bitsatcredit_discord/index.html",
        {"request": request, "user": user}
    )

@bitsatcredit_discord_ext.get("/api/v1/settings")
async def api_get_settings(user: User = Depends(check_admin)):
    """Get current settings"""
    settings = await get_settings()
    return settings

@bitsatcredit_discord_ext.post("/api/v1/settings")
async def api_update_settings(data: dict, user: User = Depends(check_admin)):
    """Update Discord bot settings"""
    await update_settings(data)
    return {"success": True}
