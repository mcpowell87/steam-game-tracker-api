from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from steamgametracker.api.steam.models import AppType


class SteamPurchase(BaseModel):
    app_id: int
    steam_id: str
    date_purchased: datetime
    name: str
    type: AppType
    price: int
    price_formatted: str
    total_playtime: Optional[int]


class PurchaseStats(BaseModel):
    total_playtime_minutes: int
    number_played: int
    percentage_played: int
    number_owned: int
    total_cost: float
    cost_per_minute: int
    recently_played: List[SteamPurchase]
