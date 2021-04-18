from binance.exceptions import BinanceAPIException, BinanceWithdrawException
from binance.client import Client
import math

def sortByLowestPriceToBuy(prices):

    l = []
    for price in prices:
        if 'USDC' in price['symbol']:
            l.append(price)

    return sorted(l, key = lambda i: i['price'])

def buyLowestSetOCO(client, debugMode=False, coinsToBuy=5):
    balance = float(client.get_asset_balance(asset='USDC')['free']) #in USD

    balance = 100 if debugMode else balance
    print("USD BALANCE IS " + str(balance))

    prices = client.get_all_tickers()
    toOrder = sortByLowestPriceToBuy(prices)
    currenciesToBuy = coinsToBuy
    bought = 0

    for price in toOrder:
        info = client.get_symbol_info(price['symbol'])
        
        if('STOP_LOSS_LIMIT' not in info['orderTypes']):
            print("\nCURRENCY DOES NOT HAVE OCO SUPPORT! TRYING NEXT!\n")
            continue

        print("---\nCOIN: " + price['symbol'])

        cost = float(price['price'])
        toBuy = int((balance / currenciesToBuy) / cost)

        print("trying to buy " + str(toBuy) + " at " + str(cost) + " for " + str(toBuy * cost) + " USD")

        try:
            if debugMode:
                print("FAKE ORDER!")
                order = client.create_test_order(symbol=price['symbol'], side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=toBuy)
            else:
                order = client.create_order(symbol=price['symbol'], side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=toBuy)
        except BinanceAPIException as e:
            print("could not buy " + price['symbol'])
            print(e)
            continue
        
        print("CREATING OCO %200 / %50")

        try:
            if not debugMode:
                order = client.order_oco_sell(symbol=price['symbol'], stopLimitTimeInForce='GTC',quantity=toBuy,stopLimitPrice=str(truncate(cost/2, 3)),stopPrice=str(truncate(cost/2, 3)),price=str(truncate(cost*2, 3)))
            else:
                print("DEBUG MODE ACTIVE, NOT ACTUALLY MAKING OCO")
        except BinanceAPIException as e:
            print("COULD NOT MAKE OCO ORDER, PLEASE DO MANUALLY FOR NOW")
            print(e)

        bought += 1
        if bought > currenciesToBuy:
            break

def checkShouldSell(client):
    tradables = getTradables(client)
    for coin in tradables:
        print(coin)

def getTradables(client):
    out = []
    for currency in client.get_account()['balances']:
        if float(currency['free']) + float(currency['locked']) > 0:
            out.append(currency) 
    return out


## https://kodify.net/python/math/truncate-decimals/
def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor