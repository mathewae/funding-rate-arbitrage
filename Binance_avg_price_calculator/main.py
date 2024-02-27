import os
from dotenv import load_dotenv
from binance.client import Client
from datetime import datetime, timedelta
from get_avg_price_hyper import get_average_price_hyper
from get_avg_price_spot_binance import get_average_price_spot_binance
from get_avg_price_futures_binance import get_average_price_futures
import requests
import json

# asset = "CYBER"
# side = "Buy"
# days_back = 4/24
# account = 2

asset = "UNI"
side = "BUY"
days_back = 1

get_average_price_futures(asset, side, days_back)

# url = "https://api.hyperliquid.xyz/info"
# headers = {"accept": "application/json"}
#
# data_pos = {
#     "type": "userFills",
#     "user": "0x1939286838F986871e7A2d24253A8d01a7c2528e",
# }
#
# response = requests.post(url, json=data_pos, headers=headers)
# print(json.dumps(response.json(), indent=4))