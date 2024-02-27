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
