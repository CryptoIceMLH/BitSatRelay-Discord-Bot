from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_admin
from lnbits.helpers import template_renderer

from .crud import get_settings

# Generic (non-API) routes
bitsatcredit_discord_generic_router: APIRouter = APIRouter()


def bitsatcredit_discord_renderer():
    return template_renderer(["bitsatcredit_discord/templates"])


@bitsatcredit_discord_generic_router.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_admin)):
    """Admin page - Discord bot settings"""
    settings = await get_settings() or {}
    return bitsatcredit_discord_renderer().TemplateResponse(
        "bitsatcredit_discord/index.html",
        {"request": request, "user": user.json(), "settings": settings}
    )
