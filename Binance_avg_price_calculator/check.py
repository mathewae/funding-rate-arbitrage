import requests
import pandas as pd
from dotenv import load_dotenv
import os
from binance.client import Client
import time

load_dotenv()

def futures_balance():
    client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))
    res = client.get_exchange_info()
    info = client.futures_account()
    info = info.get("positions")
    data = []
    for i in range(len(info)):
        if float(info[i].get("positionAmt")) > 0:
            data.append({"ticker": info[i].get("symbol"),
                         "size": info[i].get("positionAmt"), })
    data = pd.DataFrame(data)
    funding_data = client.futures_income_history(incomeType="FUNDING_FEE")
    cum_funding_data = []
    for i in range(len(funding_data)):
        if funding_data[i].get("incomeType") == "FUNDING_FEE":
            cum_funding_data.append({"ticker": funding_data[i].get("symbol"),
                                     "income": funding_data[i].get("income"), })
    df = pd.DataFrame(cum_funding_data)
    df['income'] = pd.to_numeric(df['income'])

    grouped_data = df.groupby('ticker').agg({'income': 'sum'}).reset_index()
    merged_data = pd.merge(data, grouped_data, on='ticker', how='inner')
    return (merged_data)