import asyncio
from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import wait_for_discord_updates
from .views import bitsatcredit_discord_generic_router
from .views_api import bitsatcredit_discord_api_router

# Combine routers
bitsatcredit_discord_ext: APIRouter = APIRouter(
    prefix="/bitsatcredit_discord", tags=["BitSatCredit Discord"]
)
bitsatcredit_discord_ext.include_router(bitsatcredit_discord_generic_router)
bitsatcredit_discord_ext.include_router(bitsatcredit_discord_api_router)

# Static files registration
bitsatcredit_discord_static_files = [
    {
        "path": "/bitsatcredit_discord/static",
        "name": "bitsatcredit_discord_static",
    }
]

# Task management
scheduled_tasks: list[asyncio.Task] = []

def bitsatcredit_discord_stop():
    """Stop all background tasks when extension unloads"""
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)

def bitsatcredit_discord_start():
    """Start Discord bot task when extension loads"""
    task = create_permanent_unique_task("ext_bitsatcredit_discord", wait_for_discord_updates)
    scheduled_tasks.append(task)

__all__ = [
    "db",
    "bitsatcredit_discord_ext",
    "bitsatcredit_discord_start",
    "bitsatcredit_discord_stop",
    "bitsatcredit_discord_static_files",
]
