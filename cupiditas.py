## TODO
## ADD ABILITY TO CHECK IF SHOULD SELL ON LOSS OR PROFIT, 24 HR PERIOD. 200 PERCENT PROFIT OR 50 PERCENT LOSS
## SAVE TO JSON

import os
from dotenv import load_dotenv
from binance.client import Client
import cuptools

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

client = Client(API_KEY, API_SECRET)

cuptools.buyLowestSetOCO(client, True)

cuptools.checkShouldSell(client)