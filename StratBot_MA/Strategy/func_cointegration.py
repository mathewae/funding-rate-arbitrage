from pprint import pprint
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
from statsmodels.tools.sm_exceptions import CollinearityWarning
from config_strategy_api import z_score_window
import math
import numpy as np
import pandas as pd
import warnings

def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()
    x = df.rolling(center=False, window=1).mean()
    df["ZSCORE"] = (x - mean) / std

    return df["ZSCORE"].astype(float).values

def calculate_spread(series_1, series_2, hedge_ratio):
    spread  = pd.Series(series_1) - pd.Series(series_2)*hedge_ratio
    return spread

def calculate_cointegration(series_1, series_2):

    # OPTIMIZATION - add try-except for 0-division
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=RuntimeWarning)
            # warnings.simplefilter("error", category=UserWarning)
            warnings.simplefilter("error", category=CollinearityWarning)

            coint_flag = 0
            coint_res = coint(series_1, series_2)
            coint_t = coint_res[0]
            p_value = coint_res[1]
            critical_value = coint_res[2][1]
            model = sm.OLS(series_1, series_2).fit()
            hedge_ratio = model.params[0]
            spread = calculate_spread(series_1, series_2, hedge_ratio)
            zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])
            if p_value < 0.5 and coint_t < critical_value:
                coint_flag = 1
            return (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), hedge_ratio, zero_crossings)
    except (RuntimeWarning, ValueError, CollinearityWarning) as e:
        # Handle division by zero
        # print(f"Warning: {e}")
        # You might want to return a special value or take other actions here
        return (0, None, None, None, None, None)

def extract_close_prices(prices):

    # OPTIMIZATION - file parcing

    close_prices = []
    for price_values in prices["result"]["list"]:
        # if price_values[4].replace(',', '').isdigit():
        #     return []
        # else:
        #     close_prices.append(price_values[4])

        try:
            close_prices.append(float(price_values[4]))
        except:
            return []

    return close_prices

def get_cointegrated_pairs(prices):

    coint_pair_list = []
    included_list = []

    for sym_1 in prices.keys():
        # print(sym_1)

        for sym_2 in prices.keys():
            if sym_2 != sym_1:
                sorted_characters = sorted(sym_1 + sym_2)
                unique = "".join(sorted_characters)
                if unique in included_list:
                    break

                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])

                coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossings = calculate_cointegration(series_1, series_2)
                # print(coint_t, p_value)
                if coint_flag == 1:
                    included_list.append(unique)
                    coint_pair_list.append({
                        "sym_1" : sym_1,
                        "sym_2" : sym_2,
                        "p_value" : p_value,
                        "t_value" : t_value,
                        "c_value" : c_value,
                        "hedge_ratio" : hedge_ratio,
                        "zero_crossings" : zero_crossings,
                    })

    df_coint = pd.DataFrame(coint_pair_list)
    df_coint = df_coint.sort_values("zero_crossings", ascending=False)
    df_coint.to_csv("2_cointegrated_pairs.csv", sep = ';')
    return df_coint
