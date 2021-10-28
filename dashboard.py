import streamlit as st
import plotly_express as px
import market_data
import extract_news
import prettyprint_news_watson
import plotly.graph_objects as go
from query_rewrite import get_discovery_instance, run_query
import dash_daq as daq
import news_query

st.set_page_config(layout="wide")
st.title('Crypto Dashboard')

curr_coin_symbol = st.selectbox('Select one coin', market_data.coin_list)

df_coin, df_time = market_data.obtain_market_data()

col1, col2, col3 = st.columns(3)

gauge_fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 4,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': f"{curr_coin_symbol} Score"},
    gauge = {'axis': {'range': [None, 10]},
             'steps' : [
                 {'range': [0, 5], 'color': "lightgray"},
                 {'range': [5, 10], 'color': "gray"}]}))

st.plotly_chart(gauge_fig)

# Plot Open Price
df_to_plot = df_time[df_time['asset_symbol'] == curr_coin_symbol]
fig = go.Figure(data=[go.Candlestick(x=df_to_plot['time'],
                open=df_to_plot['open'], high=df_to_plot['high'],
                low=df_to_plot['low'], close=df_to_plot['close'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=True, title=f'{curr_coin_symbol} Price')
col1.plotly_chart(fig)

# dis_instance = get_discovery_instance()

# st.write(run_query(dis_instance, 'bitcoin', '10'))

# st.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='open'))
# Plot Volatility
col2.plotly_chart(px.scatter(df_time[df_time['asset_symbol'] == curr_coin_symbol], x='time', y='volatility', title=f'{curr_coin_symbol} Volatility'))
news_md, news_senti_labels = prettyprint_news_watson.prettyprint(news_query.get_news(curr_coin_symbol), 10)
st.write(news_md, unsafe_allow_html=True)
col3.plotly_chart(px.histogram(news_senti_labels))