import logging
from typing import List
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from steamgametracker.api.steam.models import (
    PlayerSummary,
    SteamApp,
    OwnedGamesResponse,
)
from steamgametracker.api.steam.helpers import (
    get_steam_app,
    get_owned_games,
    get_player_summary,
    get_steam_apps,
)

router = InferringRouter()


@cbv(router)
class SteamRouter:
    @router.get("/apps", operation_id="getAllApps")
    def get_steam_apps(self) -> List[SteamApp]:
        return get_steam_apps()

    @router.get("/app/{app_id}", operation_id="getApp")
    def get_steam_app(self, app_id: int) -> SteamApp:
        return get_steam_app(app_id)

    @router.get("/player/{steam_id}/apps", operation_id="getOwnedGames")
    def get_owned_games(self, steam_id: int) -> OwnedGamesResponse:
        return get_owned_games(steam_id)

    @router.get("/player/{steam_id}", operation_id="getPlayer")
    def get_player(self, steam_id: int) -> PlayerSummary:
        return get_player_summary(steam_id)
