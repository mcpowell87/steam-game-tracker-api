from fastapi import HTTPException, status
from typing import List
from steamgametracker.api.purchases.models import SteamPurchase, PurchaseStats
from steamgametracker.api.purchases.dao import (
    create_purchase,
    get_purchases_by_search_term,
    get_purchases_in_range,
    get_all_purchases,
)
from steamgametracker.api.steam.helpers import get_owned_games


def get_purchases(
    steam_id: str, start: str = None, end: str = None, search: str = None
) -> List[SteamPurchase]:
    """
    Gets a list of purchases given a steam id and various filters

    Args:
        steam_id (str): The steam id to look up purchases for
        start (str, optional): Start date. Defaults to None.
        end (str, optional): End date. Defaults to None.
        search (str, optional): Search term. Defaults to None.

    Returns:
        List[SteamPurchase]: A list of matching steam purchases
    """
    if not start and not end and not search:
        return get_all_purchases(steam_id)
    elif search:
        return get_purchases_by_search_term(steam_id, search)
    else:
        return get_purchases_in_range(steam_id, start, end)


def get_purchase_stats(steam_id: str) -> PurchaseStats:
    """
    Calculates and returns purchase statistics for a steam user

    Args:
        steam_id (str): The steam id to calculate stats for

    Returns:
        PurchaseStats: A PurchaseStats response
    """
    owned_games_response = get_owned_games(steam_id)
    owned_games = {x.appid: x for x in owned_games_response.games}
    purchases = get_purchases(steam_id)

    total_cost = 0
    number_played = 0
    total_playtime = 0
    played_list: List[SteamPurchase] = []
    for purchase in purchases:
        if purchase.price:
            total_cost += purchase.price
        playtime = (
            owned_games[purchase.app_id].playtime_forever
            if purchase.app_id in owned_games
            else 0
        )
        if playtime > 0:
            number_played += 1
            purchase.total_playtime = playtime
            played_list.append(purchase)
            total_playtime += playtime

    total_cost_rounded = round(total_cost / 100.00, 2)
    cost_per_minute = (
        round(total_cost / total_playtime, 2)
        if total_playtime > 0
        else total_cost_rounded
    )
    percentage_played = (
        round((number_played / owned_games_response.game_count) * 100, 2)
        if owned_games_response.game_count > 0
        else 0
    )

    return PurchaseStats(
        total_cost=total_cost_rounded,
        number_owned=owned_games_response.game_count,
        number_played=number_played,
        total_playtime_minutes=total_playtime,
        played_list=played_list,
        cost_per_minute=cost_per_minute,
        percentage_played=percentage_played,
        recently_played=[],
    )


def add_purchase(purchase: SteamPurchase) -> None:
    """
    Adds a purchase to the database

    Args:
        purchase (SteamPurchase): A steam purchase
    """
    create_purchase(purchase)
