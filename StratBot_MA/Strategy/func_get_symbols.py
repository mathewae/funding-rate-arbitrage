from config_strategy_api import session_auth, session_unauth
from pprint import pprint

def get_tradeable_symbols():
    sym_list = []
    symbols_fees = session_auth.get_fee_rates(
        category = "spot"
    )
    symbols_info = session_auth.get_instruments_info(
        category = "spot"
    )

    symbols_info = symbols_info["result"]
    for symbol in symbols_info["list"]:
        if symbol["quoteCoin"] == "USDT" and symbol["status"] == "Trading":
            # float(symbol["maker_fee"]) < 0.001
            sym_list.append(symbol)
    return(sym_list)
