## TODO
## SAVE TO JSON?

import os
from dotenv import load_dotenv
from binance.client import Client
import cuptools

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

client = Client(API_KEY, API_SECRET)

cuptools.buyLowestSetOCO(client, False, 1)

cuptools.checkShouldSell(client)