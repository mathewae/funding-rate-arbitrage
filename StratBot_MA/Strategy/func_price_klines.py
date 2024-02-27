from config_strategy_api import session_auth, session_unauth
from config_strategy_api import timeframe
from config_strategy_api import kline_limit
import datetime
import time
from pprint import pprint


time_start_date = 0
if timeframe == 60:
    time_start_date = datetime.datetime.now()-datetime.timedelta(hours=kline_limit)
if timeframe == "D":
    time_start_date = datetime.datetime.now()-datetime.timedelta(hours=kline_limit)
time_start_seconds = int(time_start_date.timestamp())

def get_price_klines(symbol):
    prices = session_unauth.get_kline(
        category = "spot",
        symbol = symbol,
        interval = timeframe,
        limit =kline_limit,
        from_time = time_start_seconds
    )

    time.sleep(0.1)
    # print(prices["result"])
    if len(prices["result"]["list"]) != kline_limit:

        return []


    return prices

    # pprint(prices)