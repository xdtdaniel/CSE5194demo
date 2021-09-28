from newsapi import NewsApiClient
import json

key = '62187b5c441141f3a3d0de1d242b5062'
# Init
newsapi_instance = NewsApiClient(api_key=key)


def searchCryptoNews(start_date, end_date):
    all_articles = newsapi_instance.get_everything(q='cryptocurrency',
                                                   from_param=start_date,
                                                   to=end_date,
                                                   language='en',
                                                   sort_by='popularity')
    articles = all_articles['articles']
    # printing out the titles of all the articles
    # for x , y in enumerate(articles):
    #   print(f'{x} {y["title"]}')
    # printing out the keys of all the articles
    # for key, value in articles[0].items():
    #    print(f"\n{key.ljust(15)} {value}")
    with open('articles.txt', 'w') as outfile:
        json.dump(articles, outfile)
    return articles
