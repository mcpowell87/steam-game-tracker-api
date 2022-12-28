import logging
import uvicorn
from fastapi import FastAPI

# from steamgametracker import injector
from steamgametracker.config import settings
from steamgametracker.api.steam import router as steam_router
from steamgametracker.api.purchases import router as purchase_router

API_V1 = "/api/{}"

app = FastAPI(
    title="Steam Game Tracker API",
    openapi_url=API_V1.format("openapi.json"),
    docs_url=API_V1.format("docs"),
)

# app.add_event_handler("startup", injector.configure)

app.include_router(
    steam_router.router, prefix=API_V1.format("steam"), tags=["steam"]
)
app.include_router(
    purchase_router.router,
    prefix=API_V1.format("purchases"),
    tags=["purchases"],
)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(
        "steamgametracker.app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        log_level="debug",
        debug=True,
    )
