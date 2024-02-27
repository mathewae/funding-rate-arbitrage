import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
from func_cointegration import get_cointegrated_pairs
from func_cointegration import calculate_zscore
from func_plot_trends import plot_trends
import pandas as pd
import json

if __name__ == "__main__":

    # print("Getting symbols...")
    # sym_response = get_tradeable_symbols()
    #
    # print("Constructing and saving price history...")
    # if len(sym_response) > 0:
    #     store_price_history(sym_response)

    # print("Calculating co-integration...")
    # with open("1_price_list.json") as json_file:
    #     price_data = json.load(json_file)
    #     if len(price_data) > 0:
    #         coint_pairs = get_cointegrated_pairs(price_data)

    print("Plotting...")
    symbol_1 = "MATICUSDT"
    symbol_2 = "ETHUSDT"
    with open("1_price_list.json") as json_file:
        price_data = json.load(json_file)
        if len(price_data) > 0:
            plot_trends(symbol_1, symbol_2, price_data)