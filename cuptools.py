from binance.exceptions import BinanceAPIException, BinanceWithdrawException
from binance.client import Client

def sortByLowestPriceToBuy(prices):

    l = []
    for price in prices:
        if 'BUSD' in price['symbol']:
            l.append(price)

    return sorted(l, key = lambda i: i['price'])

def buyLowestSetOCO(client, debugMode=False):
    balance = client.get_asset_balance(asset='BUSD') #in USD

    balance = 100 if debugMode else balance
    print("USD BALANCE IS " + str(balance))

    prices = client.get_all_tickers()
    toOrder = sortByLowestPriceToBuy(prices)
    currenciesToBuy = 5
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
            order = client.create_test_order(symbol=price['symbol'], side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=toBuy)
        except BinanceAPIException as e:
            print("could not buy " + price['symbol'])
            print(e)
            continue
        
        print("CREATING OCO %200 / %50")

        try:
            order = client.create_oco_order(symbol=price['symbol'],side=Client.SIDE_SELL,quantity=toBuy,stopPrice=str(cost/2),price=str(cost*2))
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