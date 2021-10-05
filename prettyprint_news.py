from transformers import pipeline

def prettyprint(json_list, top_n):
    top_news = json_list[:top_n]
    md = ''
    label_map = {'LABEL_0': 'Negative', 'LABEL_1': 'Neutral', 'LABEL_2': 'Positive'}
    classifier = pipeline('sentiment-analysis', model="cardiffnlp/twitter-roberta-base-sentiment")
    for news_item in top_news:
        title = news_item['title']
        description = news_item['description']
        result = classifier(description)
        sentiment_score = result[0]['score']
        sentiment_label = label_map[result[0]['label']]
        url = news_item['url']
        md += f'## [{title}]({url})\n\n#### Sentiment: {sentiment_label}, Confidence: {sentiment_score} \n\n<span style="font-size:1.3em;"> {description} </span>\n\n---\n\n'
    return md
