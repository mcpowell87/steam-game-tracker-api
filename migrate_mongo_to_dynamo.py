from pymongo import MongoClient
from steamgametracker.api.purchases.dao import create_purchase
from steamgametracker.api.purchases.models import SteamPurchase
from steamgametracker.api.steam.helpers import get_steam_app


def migrate() -> None:
    client = MongoClient("mongodb://<user>:<pass>@database.home:27017")

    # Database Name
    db = client["steamTracking"]

    # Collection Name
    col = db["purchases"]

    purchases = col.find()

    for purchase in purchases:
        try:
            steam_purchase = SteamPurchase(
                app_id=purchase["appId"],
                name=purchase["name"],
                type=purchase["type"],
                price=purchase["price"],
                price_formatted=purchase["priceFormatted"],
                date_purchased=purchase["datePurchased"],
                steam_id=purchase["steamId"],
            )
            print(f'Adding {purchase["appId"]} to dynamo')
            create_purchase(steam_purchase)
        except:  # noqa E722
            with open("bad.txt", "a") as bad_file:
                bad_file.write(f'{purchase["appId"]}\n')
            """
            try:
                res = get_steam_app(purchase["appId"])
                print(res)
                steam_purchase = SteamPurchase(
                    app_id=purchase["appId"],
                    name=purchase["name"] if "name" in purchase else res.name,
                    type=purchase["type"] if "type" in purchase else res.type,
                    price=purchase["price"] if "price" in purchase else res.price_overview.final if res.price_overview else 0,
                    price_formatted=purchase["priceFormatted"] if "priceFormatted" in purchase else res.price_overview.final_formatted if res.price_overview else "$0",
                    date_purchased=purchase["datePurchased"],
                    steam_id=purchase["steamId"]
                )
            except:
                print(f'{purchase["appId"]} is REALLY fucked')
            """


migrate()
