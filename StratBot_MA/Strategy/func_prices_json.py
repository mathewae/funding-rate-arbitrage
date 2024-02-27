from func_price_klines import get_price_klines
import json
from pprint import  pprint

def store_price_history(symbols):

    counts = 0
    price_history_dict = {}
    for sym in symbols:
        symbol_name = sym["symbol"]
        # print(symbol_name)
        price_history = get_price_klines(symbol_name)

        if len(price_history) > 0:
            price_history_dict[symbol_name] = price_history
            counts += 1

            print(f"{counts} items stored")
        else:
            print(f"{counts} items not stored")

    if len(price_history_dict) > 0:
        with open("1_price_list.json", "w") as fp:
            json.dump(price_history_dict, fp, indent = 4)
        print("Prices saved!")


        # counts += 1
        # if counts > 5:
        #     break
        # pprint(price_history)
