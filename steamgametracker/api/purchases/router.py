from typing import List
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from steamgametracker.api.purchases.models import SteamPurchase, PurchaseStats
from steamgametracker.api.purchases.helpers import (
    get_purchases,
    get_purchase_stats,
    add_purchase,
)

router = InferringRouter()


@cbv(router)
class PurchasesRouter:
    @router.get("/{steam_id}", operation_id="get_purchases")
    def get_purchases(
        self,
        steam_id: str,
        start: str = None,
        end: str = None,
        search: str = None,
    ) -> List[SteamPurchase]:
        return get_purchases(
            steam_id=steam_id, start=start, end=end, search=search
        )

    @router.get("/{steam_id}/stats", operation_id="get_purchase_stats")
    def get_purchase_stats(self, steam_id: str) -> PurchaseStats:
        return get_purchase_stats(steam_id)

    @router.post("/", operation_id="add_purchase")
    def add_purchase(self, request: SteamPurchase) -> None:
        add_purchase(request)
