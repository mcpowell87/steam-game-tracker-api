import requests
import logging
from fastapi import HTTPException, status
from typing import List
from steamgametracker.config import settings
from steamgametracker.api.steam.models import (
    SteamApp,
    SteamAppListResponse,
    OwnedGamesResponse,
    PlayerSummary,
)


def get_steam_apps() -> List[SteamApp]:
    """
    Gets a list of all steam apps.

    Returns:
        List[SteamApp]: A list of steam apps.
    """
    r = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    json = r.json()
    response = SteamAppListResponse(**json["applist"])
    return response.apps


def get_steam_app(app_id: int) -> SteamApp:
    """
    Gets steam app details for a given app id.
    This calls an 'undocumented' store api, which is rate limited
    to roughly 1 call every second.

    Args:
        id (int): The steam app id

    Returns:
        SteamAppDetails: App details for the app
    """
    r = requests.get(
        f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=us&l=en"
    )
    response = r.json()
    if not response[str(app_id)]["success"]:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Cannot find app id {app_id}"
        )
    return SteamApp(**response[str(app_id)]["data"])


def get_owned_games(steam_id: int) -> OwnedGamesResponse:
    """
    Gets a list of games owned by the steam user id

    Args:
        steam_id (int): Steam user id to get owned games for
    """
    r = requests.get(
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={settings.STEAM_API_KEY}&steamid={steam_id}&format=json"
    )
    response = r.json()
    return OwnedGamesResponse(**response["response"])


def get_player_summary(steam_id: int) -> PlayerSummary:
    """
    Gets the player summary for a steam id

    Args:
        steam_id (int): The steam id

    Returns:
        PlayerSummary: The player summary
    """
    r = requests.get(
        f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0001/?key={settings.STEAM_API_KEY}&steamids={steam_id}&format=json"
    )
    response = r.json()
    summaries = {
        x["steamid"]: PlayerSummary(**x)
        for x in response["response"]["players"]["player"]
    }
    if str(steam_id) not in summaries:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Cannot find summary for steam id {steam_id}",
        )
    return summaries[str(steam_id)]
