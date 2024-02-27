import requests
import pandas as pd
from binance.client import Client
import os

BINANCE_API_KEY = "key"
BINANCE_API_SECRET = "secret"

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

url = f"https://api.hyperliquid.xyz/info"
headers = {"accept": "application/json"}


info = client.get_account()
balance = client.get_asset_balance(asset='USDT')
print(balance)
def get_all_positions(account):
    data = {
        "type": "clearinghouseState",
        "user": account,
    }

    response = requests.post(url, json=data, headers=headers)
    data = (response.json())
    all_positions = []
    for position in range(len(data.get("assetPositions"))):
        all_positions.append({
            "coin": data.get("assetPositions")[position].get("position").get("coin"),
            "cumFunding": round(
                -float(data.get("assetPositions")[position].get("position").get("cumFunding").get("allTime")), 4),
            "size": float(data.get("assetPositions")[position].get("position").get("szi")),
        })

    return pd.DataFrame(all_positions)


def get_all(accounts):
    all_positions = []
    for i in range(len(accounts)):
        data = {
            "type": "clearinghouseState",
            "user": accounts[i],
        }

        response = requests.post(url, json=data, headers=headers)
        data = (response.json())
        for position in range(len(data.get("assetPositions"))):
            all_positions.append({
                "coin": data.get("assetPositions")[position].get("position").get("coin"),
                "cumFunding": round(
                    -float(data.get("assetPositions")[position].get("position").get("cumFunding").get("allTime")), 4),
                "size": (data.get("assetPositions")[position].get("position").get("szi")),
            })

    # Преобразование данных в DataFrame
    df = pd.DataFrame(all_positions)

    # Конвертирование нужных полей в числовой тип
    for col in ['cumFunding', 'size']:
        df[col] = pd.to_numeric(df[col])

    # Группировка по 'coin' и суммирование остальных столбцов
    grouped_data = df.groupby('coin').agg({'cumFunding': 'sum', 'size': 'sum'}).reset_index()

    # Преобразование результата обратно в список словарей
    result = grouped_data.to_dict(orient='records')

    return pd.DataFrame(result)
