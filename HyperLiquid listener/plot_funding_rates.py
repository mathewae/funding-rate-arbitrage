import requests
import numpy as np
import pandas as pd
from binance.client import Client
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
from matplotlib.dates import DateFormatter
import io
from matplotlib.ticker import FuncFormatter

def plot_funding_rates(coin, time_frame):

    pair = coin + "USDT"
    limit = int(time_frame*(24/get_funding_rates_binance_period(pair)))

    days_back = time_frame
    time1 = int(time.time() * 1000) - 1000*60*60*24*(days_back)
    if days_back > 6:
        days_back_str = "days"
        mkr_size = 3
    elif days_back > 2:
        days_back_str = "days"
        mkr_size = 4
    else:
        days_back_str = "day"
        mkr_size = 5

    data_funding_binance = get_funding_rates_binance(pair, limit)
    data_funding_hyper = get_funding_rates_hyper(coin, time1)

    x = [100*365*24 * float(item["fundingRate"]) / float(get_funding_rates_binance_period(pair)) for item in data_funding_binance]
    funding_rates_binance = np.repeat(x, int(get_funding_rates_binance_period(pair)))
    times_binance = [datetime.fromtimestamp(item["fundingTime"] / 1000) for item in data_funding_binance]

    funding_rates_hyper = [100*365*24 * float(item["fundingRate"]) for item in data_funding_hyper]
    times_hyper = [datetime.fromtimestamp(item["time"] / 1000) for item in data_funding_hyper]  # Convert to datetime

    selected_ticks = select_ticks(times_hyper, time_frame*1.2)
    date_labels = [time.strftime('%b-%d-%Hh') for time in selected_ticks]
    avg_funding_rate_hyper = round(sum(funding_rates_hyper) / len(funding_rates_hyper))
    avg_funding_rate_binance = round(sum(funding_rates_binance) / (float(get_funding_rates_binance_period(pair))*len(funding_rates_binance)))
    avg_result = avg_funding_rate_hyper - avg_funding_rate_binance

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(times_hyper, funding_rates_hyper, marker='.', markersize=mkr_size, color='darkblue', linestyle='--', alpha=0.3)
    plt.plot(times_hyper, funding_rates_binance, marker='.', markersize=mkr_size, color='darkorange', linestyle='--', alpha=0.3)
    plt.plot(times_hyper, funding_rates_hyper-funding_rates_binance, marker='o', markersize=mkr_size, color='red', linestyle='--')
    plt.title(r'$\bf{' + coin + '}$' + ' funding rates over last ' + str(time_frame) + " "+days_back_str)
    plt.ylabel('Funding rate, % annually (extrapolated)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    plt.text(0.995, 0.985, "avg_hyper=" + str(avg_funding_rate_hyper) + " %", fontsize=10, color='darkblue',
             ha='right', va='top',
             transform=plt.gca().transAxes)
    plt.text(0.995, 0.95, "avg_binance=" + str(avg_funding_rate_binance) + " %", fontsize=10, color='darkorange',
             ha='right', va='top',
             transform=plt.gca().transAxes)
    plt.text(0.995, 0.915, "avg_result=" + str(avg_result) + " %", fontsize=10, color='red',
             ha='right', va='top',
             transform=plt.gca().transAxes)

    plt.xticks(selected_ticks, [time.strftime('%b-%d-%Hh') for time in selected_ticks], rotation=45)

    # Customizing grid lines to make day-separating grid lines bold
    plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.5)
    plt.axhline(y=0, color='black', linewidth=1.5)

    plt.tight_layout()
    plt.show()
    # Save the plot as an image
    # buffer = io.BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)

    # Now send buffer to Telegram as a photo

    # Example using Telepot (you may use another Telegram library)
    # import telepot
    # bot = telepot.Bot('YOUR_TELEGRAM_BOT_TOKEN')
    # bot.sendPhoto(chat_id, ('filename.png', buffer))

    return None

def select_ticks(times, time_frame):
    selected_ticks = []
    if time_frame < 7:
        for time in times:
            if time.hour in [0, 6, 12, 18]:  # Add ticks at midnight and noon
                selected_ticks.append(time)
    else:
        for time in times:
            if time.hour in [0, 12]:  # Add ticks at midnight and noon
                selected_ticks.append(time)
    return selected_ticks

def get_funding_rates_binance(symbol, limit):
    url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch funding rate history from Binance:", response.text)
        return None

def get_funding_rates_binance_period(symbol):
    url = 'https://fapi.binance.com/fapi/v1/fundingInfo'
    response = requests.get(url)
    exchange_info = response.json()
    for symbol_info in exchange_info:
        if symbol_info['symbol'] == symbol:
            return int(symbol_info['fundingIntervalHours'])

    funding_info = get_funding_rates_binance(symbol, 2)
    if len(funding_info) >= 2:
        timestamp1 = int(funding_info[0]['fundingTime']) / 1000
        timestamp2 = int(funding_info[1]['fundingTime']) / 1000

        datetime1 = datetime.utcfromtimestamp(timestamp1)
        datetime2 = datetime.utcfromtimestamp(timestamp2)

        if datetime1 and datetime2:
            time_difference_hours = (datetime2 - datetime1).total_seconds() / 3600
            return int(time_difference_hours)
        else:
            print(datetime1, datetime2)
            return None
    else:
        return None
    return None

def get_funding_rates_hyper(coin, time):
    url = f"https://api.hyperliquid.xyz/info"
    headers = {"accept": "application/json"}

    data_funding = {
        "type": "fundingHistory",
        "coin": coin,
        "startTime": time,
    }

    response = requests.post(url, json=data_funding, headers=headers)
    data_funding = (response.json())
    return data_funding

def to_percent(y, position):
    s = str(y)
    return s + '%'