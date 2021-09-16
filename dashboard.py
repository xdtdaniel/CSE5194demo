import streamlit as st
import plotly_express as px
import market_data

st.set_page_config(layout="wide")
st.write('Hello World')
df_coin, df_time = market_data.obtain_market_data()
# Plot Open Price
st.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='open'))
# Plot Volatility
st.plotly_chart(px.scatter(df_time[df_time['asset_id'] == 1], x='time', y='volatility'))
