import requests
import json
import twint
import datetime

TOKEN = "bg1nyltes7d0hzukc6vbpkh"
API = "https://api.lunarcrush.com/v2"
TWITTERSOURCE = "twitter"

def getTwitterFeed(
        key: str = TOKEN,
        symbol: str = "BTC",
        quantity: int = 100,
        sources: str = "twitter",
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
    
def getTwitterHour(
        start: int,
        symbol: str = "BTC",
        quantity: int = 100,
    ) -> float:
    tweets = getTwitterFeed(symbol=symbol, quantity=quantity, start=start, end=start+3600)
    output = {"start": start}
    totalSentiment = 0
    totalSocialScore = 0
    count = 0
    for i in tweets:
        if isinstance(i['sentiment'], int) and isinstance(i['social_score'], int):
            totalSentiment += i['sentiment'] * i['social_score']
            totalSocialScore += i['social_score']
            count += 1
    output["totalSentiment"] = totalSentiment
    output["totalSocialScore"] = totalSocialScore
    if totalSocialScore != 0:
        output["weightedSentiment"] = totalSentiment/totalSocialScore
        output["averageSentiment"] = totalSentiment/count
    else:
        output["averageSentiment"] = -1
        output["weightedSentiment"] = -1
    return output

def getTwitterData(
        start: str,
        end: str,
        symbol: str = "BTC",
        quantity: int = 100,
    ) -> list:
    startDate = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    endDate = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    current = int(startDate.timestamp())
    output = []
    while current < endDate.timestamp():
        output.append(getTwitterHour(symbol=symbol, quantity=quantity, start=current))
        current += 3600
    return output
    
    
def getTwitterSentiment(
        start: str,
        end: str,
        symbol: str = "BTC",
        quantity: int = 100,
    ) -> list:
    data = getTwitterData(symbol=symbol, quantity=quantity, start=start, end=end)
    output = []
    for p in data:
        output.append([p["start"], p["weightedSentiment"]])
    return output