import streamlit as st
import plotly_express as px
import market_data
import extract_news
import prettyprint_news
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.write('Hello World')
df_coin, df_time = market_data.obtain_market_data()

# Plot Open Price
fig = go.Figure(data=[go.Candlestick(x=df_time['time'],
                open=df_time['open'], high=df_time['high'],
                low=df_time['low'], close=df_time['close'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig)

# st.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='open'))
# Plot Volatility
st.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='volatility'))
st.write(prettyprint_news.prettyprint(extract_news.searchCryptoNews('2021-09-20', '2021-09-21'), 10), unsafe_allow_html=True)