import streamlit as st
import plotly_express as px
import market_data
import extract_news
import prettyprint_news_watson
import plotly.graph_objects as go
from query_rewrite import get_discovery_instance, run_query
import dash_daq as daq
import news_query
import pandas as pd

st.set_page_config(layout="wide")
st.title('Crypto Dashboard')

curr_coin_symbol = st.selectbox('Select one coin', market_data.coin_list)

df_coin, df_time = market_data.obtain_market_data()

reg_parameters = {'BTC': [0.00244, -0.00795], 'DOGE': [0.00173, -0.00582], 'ETH': [0.00086, -0.00271]}

col1, col2, col3 = st.columns(3)

senti_table = pd.read_csv(f'{curr_coin_symbol}_train.csv')
fig1 = px.line(x=senti_table['time'], y=senti_table['Score'])
fig2 = px.line(x=senti_table['time'], y=[senti_table['Score'].mean()] * len(senti_table['Score']))
fig2.update_traces(line_color='red')
fig3 = go.Figure(data=fig1.data + fig2.data)
fig3.update_layout(title=f'{curr_coin_symbol} Sentiment Over Time')


df_to_plot = df_time[df_time['asset_symbol'] == curr_coin_symbol]
curr_price = round(list(df_to_plot['close'])[-1], 3)
change_next = round((list(senti_table['Score'])[-1] * reg_parameters[curr_coin_symbol][0] + reg_parameters[curr_coin_symbol][1]) * 100, 3)

st.metric(label="Price Pred for Next Hr", value=f'${curr_price}', delta=f'{change_next}%')

gauge_fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 4,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': f"{curr_coin_symbol} Score"},
    gauge = {'axis': {'range': [None, 10]},
             'steps' : [
                 {'range': [0, 5], 'color': "lightgray"},
                 {'range': [5, 10], 'color': "gray"}]}))

# st.plotly_chart(gauge_fig)

# Plot Open Price

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
col3.plotly_chart(fig3)
news_md, news_senti_labels = prettyprint_news_watson.prettyprint(news_query.get_news(curr_coin_symbol), 10)
st.write(news_md, unsafe_allow_html=True)
# col3.plotly_chart(px.histogram(news_senti_labels, title='Top 50 News Sentiment'))
