from transformers import pipeline

def prettyprint(json_list, top_n):
    top_news = json_list[:top_n]
    md = ''
    label_map = {'LABEL_0': 'Negative', 'LABEL_1': 'Neutral', 'LABEL_2': 'Positive'}
    classifier = pipeline('sentiment-analysis', model="cardiffnlp/twitter-roberta-base-sentiment")
    labels = []
    
    for news_item in top_news:
        title = news_item['title']
        description = news_item['text']
        result = classifier(description)
        sentiment_score = result[0]['score']
        sentiment_label = label_map[result[0]['label']]
        labels.append(sentiment_label)
        ibm_sentiment = news_item["enriched_text"]["sentiment"]["document"]
        ibm_sentiment_label = ibm_sentiment["label"]
        ibm_sentiment_score = ibm_sentiment["score"]
        url = news_item['url']
        md += f'## [{title}]({url})\n\n#### Sentiment (Trans): {sentiment_label}, Confidence: {sentiment_score} \n\n#### Sentiment (IBM): {ibm_sentiment_label}, Confidence: {ibm_sentiment_score}\n\n<span style="font-size:1.3em;"> {description} </span>\n\n---\n\n'
    
    return md, labels

