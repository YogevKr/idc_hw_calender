from piazza_api import Piazza
from config import Config

p = Piazza()
p.user_login(email=Config.PIAZZA_EMAIL, password=Config.PIAZZA_PASSWORD)


