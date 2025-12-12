from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DiscordSettings(BaseModel):
    id: int
    bot_token: str
    enabled: bool = True
    rotation_speed: int = 30
    lnbits_api_url: str = "https://lnbits.molonlabe.holdings"
    created_at: datetime
    updated_at: datetime
