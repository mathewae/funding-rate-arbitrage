import os
from datetime import datetime, timedelta
import requests

def get_trades(account):

    # Change to you accounts
    account0 = "1"
    account1 = "2"
    account2 = "3"
    account3 = "4"
    account4 = "5"

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


