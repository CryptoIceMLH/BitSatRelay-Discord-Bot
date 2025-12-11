import asyncio
from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task

from .views import bitsatcredit_discord_ext
from .tasks import wait_for_discord_updates

# Extension metadata
db_name = "ext_bitsatcredit_discord"
bitsatcredit_discord_ext: APIRouter

# Scheduled tasks
scheduled_tasks = []

def bitsatcredit_discord_start():
    """Start Discord bot task when extension loads"""
    task = create_permanent_unique_task("ext_bitsatcredit_discord", wait_for_discord_updates)
    scheduled_tasks.append(task)
