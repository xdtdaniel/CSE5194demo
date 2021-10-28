import urllib.request
import ssl
import json
import time
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

api_key = "bg1nyltes7d0hzukc6vbpkh"

# Allows adding as many coins as desired
coin_list = [
    "DOGE",
    "BTC",
    "ETH"
]
coins = ','.join(coin_list)

map = [
    {"name": ""},
    {"symbol": ""},
    {"price": " Price: "},
    {"percent_change_24h": " - 24 Hour Percent Change: "},
    {"market_cap": " Market Cap: "},
    {"volume_24h": " 24 Hour Volume: "},
    {"url_shares": " URL Shares: "},
    {"reddit_posts": " Reddit Posts: "},
    {"tweets": " Tweets: "},
    {"galaxy_score": " Galaxy Score: "},
    {"volatility": " Volatility: "},
    {"social_volume": " Social Volume: "},
    {"news": " News: "},
    {"close": " Close: "},
    {'time': ' Time:'},
]

time_series_cols = ['asset_id', 'time', 'open', 'close', 'high', 'low', 'volatility']
data_num = 2000
fields = [list(key.keys())[0] for key in map]
coins_df = pd.DataFrame(columns=fields)
time_df = pd.DataFrame(columns=time_series_cols)


def obtain_market_data():
    url = f'https://api.lunarcrush.com/v2?data=assets&key={api_key}&symbol={coins}&data_points={data_num}'
    assets = json.loads(urllib.request.urlopen(url).read())
    global coins_df
    global time_df

    name_dict = {}
    coins_df = pd.DataFrame()
    time_df = pd.DataFrame()

    for n in range(len(coin_list)):
        data = assets['data'][n]
        name_dict[data['id']] = data['symbol']
        required_data = [{key: data[key] for key in fields}]
        time_series = data['timeSeries']

        temp_time_df = pd.DataFrame(time_series, columns=time_series_cols)
        temp_time_df['time'] = pd.to_datetime(temp_time_df['time'], unit='s')
        time_df = pd.concat([time_df, temp_time_df], ignore_index=True)
        time_df['asset_symbol'] = time_df['asset_id'].replace(name_dict, inplace=False)

        coins_df = coins_df.append(required_data, ignore_index=True)
        coins_df.at[coins_df.shape[0] - 1, 'time'] = pd.to_datetime(coins_df.iloc[coins_df.shape[0] - 1]['time'], unit='s')

    return coins_df, time_df

