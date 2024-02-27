# Documentation link - https://bybit-exchange.github.io/docs/v5/order/create-order#request-example
# Exchange link: https://testnet.bybit.com/user/assets/home/trading

from pprint import pprint
from pybit import unified_trading

mode = "test"
timeframe = 60
kline_limit = 200 #maximum from thr docs
z_score_window = 21

api_key_mainnet = ""
api_secret_mainnet = ""

api_key_testnet = "key"
api_secret_testnet = "secret"

api_key = api_key_testnet if mode == "test" else api_key_mainnet

api_key_secret = api_secret_testnet if mode == "test" else api_secret_testnet

api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"

session_unauth = unified_trading.HTTP(
    testnet=True
)

session_auth = unified_trading.HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_key_secret
)
