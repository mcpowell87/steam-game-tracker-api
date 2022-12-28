from pydantic.main import BaseModel
from typing import List, Optional

from enum import Enum


class AppType(Enum):
    GAME = "game"
    DLC = "dlc"
    DEMO = "demo"
    ADVERTISING = "advertising"
    MOD = "mod"
    VIDEO = "video"
    MUSIC = "music"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls):
        return cls(cls.UNKNOWN)


class PriceOverview(BaseModel):
    currency: str
    initial: int
    final: int
    discount_percent: int
    initial_formatted: str
    final_formatted: str


class AppCategory(BaseModel):
    id: int
    description: str


class AppGenre(BaseModel):
    id: str
    description: str


class RelatedApp(BaseModel):
    appid: Optional[int]
    name: Optional[str]
    description: Optional[str]


class SteamApp(BaseModel):
    appid: int
    name: str
    # Extented Details
    type: Optional[AppType]
    is_free: Optional[bool]
    short_description: Optional[str]
    header_image: Optional[str]
    website: Optional[str]
    developers: Optional[List[str]]
    publishers: Optional[List[str]]
    price_overview: Optional[PriceOverview]
    categories: Optional[List[AppCategory]]
    genres: Optional[List[AppGenre]]
    background: Optional[str]
    background_raw: Optional[str]
    dlc: Optional[List[int]]
    fullgame: Optional[List[RelatedApp]]
    demos: Optional[List[RelatedApp]]

    def __init__(self, appid: int = None, steam_appid: int = None, **kwargs):
        app_id = appid if appid else steam_appid
        super().__init__(appid=app_id, **kwargs)


class SteamAppListResponse(BaseModel):
    apps: List[SteamApp]


class OwnedGame(BaseModel):
    appid: int
    name: Optional[str]
    playtime_2weeks: Optional[int]
    playtime_forever: int
    img_icon: Optional[str]
    img_logo_url: Optional[str]


class OwnedGamesResponse(BaseModel):
    game_count: int
    games: List[OwnedGame]


class PersonaState(Enum):
    OFFLINE = 0
    ONLINE = 1
    BUSY = 2
    AWAY = 3
    SNOOZE = 4
    LOOKING_TO_TRADE = 5
    LOOKING_TO_PLAY = 6


class VisibilityState(Enum):
    NotVisible = 1
    Public = 3


class PlayerSummary(BaseModel):
    steamid: int
    personaname: str
    profileurl: str
    avatar: str
    avatarmedium: str
    avatarfull: str
    personastate: PersonaState
    communityvisibilitystate: VisibilityState
    profilestate: Optional[int]
    lastlogoff: Optional[int]
    commentpermission: Optional[str]
    realname: Optional[str]
    primaryclanid: Optional[str]
    timecreated: Optional[int]
    gameid: Optional[int]
    gameextrainfo: Optional[str]
    loccountrycode: Optional[str]
    locstatecode: Optional[str]
    loccityid: Optional[int]
