import requests
import json

TOKEN = "bg1nyltes7d0hzukc6vbpkh"
API = "https://api.lunarcrush.com/v2"
TWITTERSOURCE = "twitter"

def getTwitterFeed(
        key: str = TOKEN,
        symbol: str = "BTC",
        sources: str = "twitter",
        quantity: int = 100,
        itype: str = "influential",
        start: int = 0,
        end: int = 0,
    ) -> list:
    query = {"data": "feeds", "key": key, "symbol": symbol, "sources": sources, "limit": quantity, "type": itype}
    if start != 0:
        query["start"] = start
    if end != 0:
        query["end"] = end
    result = requests.get(API, params=query).text
    result = json.loads(result)
    return result["data"]

