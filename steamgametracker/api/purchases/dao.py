from typing import List
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from steamgametracker.api.purchases.models import SteamPurchase, AppType
from dateutil import parser
from datetime import timezone, datetime


class SteamPurchasesDateIndex(GlobalSecondaryIndex):
    """
    This represents the PurchasesByDate GSI
    """

    class Meta:
        index_name = "PurchasesByDate"
        read_capacity_units = 25
        write_capacity_units = 25
        projection = AllProjection()

    steam_id = UnicodeAttribute(hash_key=True)
    date_purchased = UnicodeAttribute(range_key=True)


class SteamPurchaseDynamo(Model):
    """
    DynamoDB Model for SteamPurchases
    """

    class Meta:
        table_name = "SteamPurchases"

    steam_id = UnicodeAttribute(hash_key=True)
    app_id = NumberAttribute(range_key=True)
    date_purchased = UnicodeAttribute()
    name = UnicodeAttribute(null=True)
    type = UnicodeAttribute()
    price = NumberAttribute(default=0)
    price_formatted = UnicodeAttribute(default="$0")

    date_purchased_index = SteamPurchasesDateIndex()


def create_purchase(purchase: SteamPurchase):
    """
    Creates a purchase and adds it to the database.

    Args:
        purchase (SteamPurchase): The purchase to add.
    """
    # Normalize date to UTC
    date_purchased = purchase.date_purchased.astimezone(tz=timezone.utc)

    db_purchase = SteamPurchaseDynamo(
        hash_key=purchase.steam_id,
        range_key=purchase.app_id,
        date_purchased=date_purchased.isoformat(),
        name=purchase.name,
        type=purchase.type.value,
        price=purchase.price,
        price_formatted=purchase.price_formatted,
    )
    db_purchase.save()


def get_all_purchases(steam_id: str) -> List[SteamPurchase]:
    """
    Gets a list of all purchases for a given steam user.

    Args:
        steam_id (str): The steam id of the user to get purchases for.

    Returns:
        List[SteamPurchase]: List of purchases made by a steam user.
    """
    purchases: List[SteamPurchase] = []
    for purchase in SteamPurchaseDynamo.query(steam_id):
        purchases.append(to_model(purchase))
    return purchases


def get_purchases_in_range(
    steam_id: str,
    start: str,
    end: str = None,
) -> List[SteamPurchase]:
    """
    Get purchases in a given time range.

    Args:
        steam_id (str): The steam id of the user whose purchases to search
        start (str): The start time in ISO format
        end (str, optional): The optional end time in ISO format Defaults to None.

    Returns:
        List[SteamPurchase]: A list of steam purchases.
    """
    purchases: List[SteamPurchase] = []
    start_date = parser.parse(start)
    end_date = parser.parse(end) if end else datetime.now(tz=timezone.utc)

    # handle date range
    for purchase in SteamPurchaseDynamo.date_purchased_index.query(
        steam_id,
        SteamPurchaseDynamo.date_purchased.between(start_date, end_date),
    ):
        purchases.append(to_model(purchase))
    return purchases


def get_purchases_by_search_term(
    steam_id: str, search_term: str
) -> List[SteamPurchase]:
    """
    Gets purchases based on a case insensitive search term.

    Args:
        steam_id (str): The steam id of the user whose purchases to search
        search_term (str): The search term.

    Returns:
        List[SteamPurchase]: A list of matching steam purchases.
    """
    purchases = get_all_purchases(steam_id)
    filtered: List[SteamPurchase] = []
    for purchase in purchases:
        if search_term.lower() in purchase.name.lower():
            filtered.append(purchase)
    return filtered


def to_model(db: SteamPurchaseDynamo) -> SteamPurchase:
    """
    Converts the pynamodb model to a pydantic model.

    Args:
        db (SteamPurchaseDynamo): The pynamodb model to convert

    Returns:
        SteamPurchase: A pydantic model
    """
    return SteamPurchase(
        app_id=db.app_id,
        steam_id=db.steam_id,
        date_purchased=parser.parse(db.date_purchased),
        name=db.name,
        type=AppType(db.type),
        price=db.price,
        price_formatted=db.price_formatted,
    )
