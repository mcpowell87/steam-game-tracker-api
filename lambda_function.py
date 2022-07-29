from mangum import Mangum
from steamgametracker.app import app

handler = Mangum(app)
