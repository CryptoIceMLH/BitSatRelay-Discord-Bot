from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from lnbits.core.models import User
from lnbits.decorators import check_admin

# Generic (non-API) routes
bitsatcredit_discord_generic_router: APIRouter = APIRouter()

templates = Jinja2Templates(directory="templates")

@bitsatcredit_discord_generic_router.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(check_admin)):
    """Admin page - Discord bot settings"""
    return templates.TemplateResponse(
        "bitsatcredit_discord/index.html",
        {"request": request, "user": user}
    )
