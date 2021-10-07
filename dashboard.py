import streamlit as st
import plotly_express as px
import market_data
import extract_news
import prettyprint_news
import plotly.graph_objects as go
from query_rewrite import get_discovery_instance, run_query



st.set_page_config(layout="wide")
st.title('Crypto Dashboard')
df_coin, df_time = market_data.obtain_market_data()

col1, col2 = st.columns(2)

# Plot Open Price
df_to_plot = df_time[df_time['asset_id'] == 1]
fig = go.Figure(data=[go.Candlestick(x=df_to_plot['time'],
                open=df_to_plot['open'], high=df_to_plot['high'],
                low=df_to_plot['low'], close=df_to_plot['close'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=True, title='Bitcoin Price')
col1.plotly_chart(fig)

dis_instance = get_discovery_instance()

st.write(run_query(dis_instance, 'bitcoin', '10'))

# st.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='open'))
# Plot Volatility
col2.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='volatility', title='Bitcoin Volatility'))
st.write(prettyprint_news.prettyprint(extract_news.searchCryptoNews('2021-09-20', '2021-09-21'), 10), unsafe_allow_html=True)