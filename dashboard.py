import streamlit as st
import plotly_express as px
import market_data
import extract_news
import prettyprint_news
import plotly.graph_objects as go
from transformers import pipeline

label_map = {'LABEL_0': 'Negative', 'LABEL_1': 'Neutral', 'LABEL_2': 'Positive'}

classifier = pipeline('sentiment-analysis', model="cardiffnlp/twitter-roberta-base-sentiment")
result = classifier('We are very happy to show you the 🤗 Transformers library.')
score = result[0]
label = label_map[result[0]['label']]



st.set_page_config(layout="wide")
st.title('Crypto Dashboard')
df_coin, df_time = market_data.obtain_market_data()

st.write(f'{label}, {score}')

col1, col2 = st.columns(2)

# Plot Open Price
df_to_plot = df_time[df_time['asset_id'] == 1]
fig = go.Figure(data=[go.Candlestick(x=df_to_plot['time'],
                open=df_to_plot['open'], high=df_to_plot['high'],
                low=df_to_plot['low'], close=df_to_plot['close'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=True, title='Bitcoin Price')
col1.plotly_chart(fig)

# st.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='open'))
# Plot Volatility
col2.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='volatility', title='Bitcoin Volatility'))
st.write(prettyprint_news.prettyprint(extract_news.searchCryptoNews('2021-09-20', '2021-09-21'), 10), unsafe_allow_html=True)