import os
from datetime import datetime, timedelta
import requests

def get_trades(account):

    # Change to you accounts
    account0 = "0x938eDcCc3Bfd33725443101e70398d10E35519D7"
    account1 = "0x1939286838F986871e7A2d24253A8d01a7c2528e"
    account2 = "0x76Dfe5d18078574A26ddEAA560E7031f140E264e"
    account3 = "0x0050F3427E5388E9cc458e977bC3444faf015618"
    account4 = "0x76Dfe5d18078574A26ddEAA560E7031f140E264e"

    if account ==0: account=account0
    elif account==1: account = account1
    elif account==2: account = account2
    elif account==3: account = account3
    elif account==4: account = account4

    url = "https://api.hyperliquid.xyz/info"
    headers = {"accept": "application/json"}

    data_pos = {
        "type": "userFills",
        "user": account,
    }

    response = requests.post(url, json=data_pos, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch trade data for account {account}")
        return []

def calculate_average_weighted_price(trades):
    total_cost = 0
    total_quantity = 0
    for trade in trades:
        price = float(trade['px'])
        quantity = float(trade['sz'])
        total_cost += price * quantity
        total_quantity += quantity
    if total_quantity == 0:
        return None
    else:
        return total_cost / total_quantity


def get_average_price_hyper(asset, side, days_back, account):
    if side == "Sell": side = "A"
    elif side == "Buy": side = "B"
    trades = get_trades(account)
    trades = [trade for trade in trades if trade['side'] == side]
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days_back)
    trades = [trade for trade in trades if datetime.utcfromtimestamp(trade['time'] / 1000) >= start_time]
    trades = [trade for trade in trades if trade['coin'] == asset.upper()]
    if side == "A": side = "Sell"
    elif side == "B": side = "Buy"
    if trades:
        average_price = calculate_average_weighted_price(trades)
        if average_price is not None:
            formatted_average_price = f"{average_price:.8g}"
            print(
                f"Average weighted {side} price of {asset.upper()} position on HyperLiquid for the given period: ${formatted_average_price}")
        else:
            print(f"No {side} trades on HyperLiquid found for {asset.upper()} for the given period")
    else:
        print(f"No {side} trades on HyperLiquid found for {asset.upper()} for the given period")


# asset = "PIXEL"
# side = "Sell"
# days_back = 5
# account = 0
#
# get_average_price_hyper(asset, side, days_back, account)


