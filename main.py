#!/usr/bin/env python

import requests
from pprint import pprint

import pandas as pd

from io import StringIO

def get_response_from_api():
    headers = {
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://api.londonstockexchange.com/',
        'Connection': 'keep-alive',
    }

    # https://api.londonstockexchange.com/api/gw/lse/download/POG/tearsheet
    # https://api.londonstockexchange.com/api/gw/lse/instruments/alldata/POG
    # Google: "api.londonstockexchange.com" -inurl:londonstockexchange.com bid offer

    response = requests.get('https://api.londonstockexchange.com/api/gw/lse/download/POG/trades', headers=headers)

    return response.text

def write_response_to_file(response_text: str):
    f = open("response_text", "a")
    f.write(response_text)
    f.close()

def get_response_from_file():
    f = open("response_text", "r")
    response_text = f.read()
    f.close()

    return response_text


if __name__ == "__main__":
#    trades_csv = get_response_from_file()
    trades_csv = get_response_from_api()
    write_response_to_file(trades_csv)
    csv_string_io = StringIO(trades_csv)
    df = pd.read_csv(csv_string_io, sep=",")

    df_desc = df.describe()

    num_trades = len(df)

    total_vol = sum(df['volume'])
    min_vol = min(df['volume'])
    max_vol = max(df['volume'])
    avg_vol = df['volume'].mean()

    vals = df['tradeValue']/100 # df['price']@df['volume']/100
    min_val = int(min(df['tradeValue']/100))
    max_val = int(max(df['tradeValue']/100))
    avg_val = int(df['tradeValue'].mean()) # int((df['price']*df['volume']).mean()/100)
    total_val = sum(df['tradeValue'])

    min_price = min(df['price'])
    max_price = max(df['price'])
    avg_price = (total_val * 100)/total_vol

    print(df.describe)
