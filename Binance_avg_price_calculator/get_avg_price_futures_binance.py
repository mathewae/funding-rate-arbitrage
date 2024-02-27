import os
from dotenv import load_dotenv
from binance.client import Client
from datetime import datetime, timedelta

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(api_key=api_key, api_secret=api_secret)

def calculate_average_weighted_price(trades):
    total_cost = 0
    total_quantity = 0
    for trade in trades:
        price = float(trade['price'])
        quantity = float(trade['qty'])
        total_cost += price * quantity
        total_quantity += quantity
    if total_quantity == 0:
        return None
    else:
        return total_cost / total_quantity

def get_average_price_futures(asset, side, days_back):
    side = side.upper()
    trades = client.futures_account_trades(symbol=asset.upper() + "USDT", limit=1000)
    trades = [trade for trade in trades if (trade['side'] == side)]
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days_back)
    trades = [trade for trade in trades if datetime.utcfromtimestamp(trade['time'] / 1000) >= start_time]

    if trades:
        average_price = calculate_average_weighted_price(trades)
        if average_price is not None:
            formatted_average_price = f"{average_price:.8g}"
            print(f"Average weighted {side} price of {asset.upper()}USDT position on FUTURES for the given period: ${formatted_average_price}")
        else:
            print(f"No {side} trades on FUTURES found for {asset.upper()}USDT for the given period")
    else:
        print(f"No trades on FUTURES found for {asset.upper()}USDT for the given period")

asset = "UNI"
side = "BUY"
days_back = 1

get_average_price_futures(asset, side, days_back)
