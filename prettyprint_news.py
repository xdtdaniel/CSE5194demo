def prettyprint(json_list, top_n):
    top_news = json_list[:top_n]
    md = ''
    for news_item in top_news:
        title = news_item['title']
        description = news_item['description']
        url = news_item['url']
        md += f'## [{title}]({url})\n\n<span style="font-size:1.3em;"> {description} </span>\n\n---\n\n'
    return md
