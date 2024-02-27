import requests
import pandas as pd
from binance.client import Client
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
from matplotlib.dates import DateFormatter
import io
from plot_funding_rates import plot_funding_rates, get_funding_rates_binance_period

time1 = int(time.time() * 1000) - 1000*60*60*24*(1)-1000*60*60*3

url = f"https://api.hyperliquid.xyz/info"
headers = {"accept": "application/json"}

account0 = "0x938eDcCc3Bfd33725443101e70398d10E35519D7"
account1 = "0x1939286838F986871e7A2d24253A8d01a7c2528e"
account2 = "0x76Dfe5d18078574A26ddEAA560E7031f140E264e"
account3 = "0x0050F3427E5388E9cc458e977bC3444faf015618"
account4 = "0xf394366d39128Ffe132289744FCaB4F56b22D686"

account = account2

data_state = {
    "type": "clearinghouseState",
    "user": account,
}

data_pos = {
    "type": "openOrders",
    "user": account,
}

response = requests.post(url, json=data_state, headers=headers)
data_state = (response.json())

response = requests.post(url, json=data_pos, headers=headers)
data_pos = (response.json())

# response = requests.post(url, json=data_funding1, headers=headers)
# data_funding1 = (response.json())

PnL_bycoin = []
total_pnl = 0
for position in range(len(data_state.get("assetPositions"))):
    PnL_bycoin.append({
        "coin": data_state.get("assetPositions")[position].get("position").get("coin"),
        "unrealizedPnl": round(float(data_state.get("assetPositions")[position].get("position").get("unrealizedPnl")))
        # "size": float(data.get("assetPositions")[position].get("position").get("szi")),
    })
    total_pnl = total_pnl + round(float(data_state.get("assetPositions")[position].get("position").get("unrealizedPnl")))

print("\n ACCOUNT INFORMATION", json.dumps(data_state, indent=4))
print("\n OPEN POSITIONS", json.dumps(data_pos, indent=4))
count = 0
for i in data_pos:
    count = count+1
print(count)

print("\n PnL", json.dumps(PnL_bycoin, indent=4), "\n Total PnL ", total_pnl)

# print("\n FUNDING RATES HISTORY", json.dumps(data_funding1, indent=4))
# plot_funding_rates("Zeta",1)
# print(get_funding_rates_binance_period("COMBOUSDT"))