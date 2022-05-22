"""
Created on Wed Nov 17 09:19:21 2021
@author: Juan
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
#from datetime import datetime


#1.-----Downloads data
df = pd.read_csv("https://raw.githubusercontent.com/juandavid7777/Bitcoin_projectedPriceVSCummulativeInterest/main/BTC_price_cummulative.csv", parse_dates = ["Date"])


#2.-----API token definition
coin_name = "BTC"
projected_days = 180

st.write(1234)
#3.-----Plots figures

#=================================================== BANDS CHART===========================================
# fig = go.Figure()

# #Price candlesticks plots
# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["close"],
#     mode = 'lines',
#     name = '',
#     line = dict(width = 0.5, color = "white")
#     ))

# fig.add_trace(go.Candlestick(
#     x=df['Date'],
#     open=df['open'],
#     high=df['high'],
#     low=df['low'],
#     close=df['close'],
#     name = coin_name + ' price'
#     ))

# #Prices for uncertainity bands
# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["trace_3"],
#     mode = 'lines',
#     name = '99.9%',
#     line = dict(width = 0.5, dash = 'dash', color = "red"),
#     ))

# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["trace_2"],
#     mode = 'lines',
#     name = '97.8%',
#     line = dict(width = 0.5, dash = 'dash', color = "yellow"),
#     fill='tonexty',
#     fillcolor='rgba(245, 66, 66,0.2)'  #Red
#     ))

# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["trace_1"],
#     mode = 'lines',
#     name = '84.2%',
#     line = dict(width = 0.5, dash = 'dash', color = "green"),\
#     fill='tonexty',
#     fillcolor='rgba(245, 230, 66,0.2)'  #yellow
#     ))

# #Prices regression plot
# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["trace_0"],
#     mode = 'lines',
#     name = '50.0%',
#     line = dict(width = 1.0, dash = 'dash', color = "grey"),
#     fill='tonexty',
#     fillcolor='rgba(0, 199, 56,0.2)'  #green
#     ))

# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["trace_-1"],
#     mode = 'lines',
#     name = '15.8%',
#     line = dict(width = 0.5, dash = 'dash', color = "green"),
#     fill='tonexty',
#     fillcolor='rgba(0, 199, 56,0.2)'  #green
#     ))

# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["trace_-2"],
#     mode = 'lines',
#     name = '2.2%',
#     line = dict(width = 0.5, dash = 'dash', color = "yellow"),
#     fill='tonexty',
#     fillcolor='rgba(245, 230, 66,0.2)'  #Yellow
#     ))

# fig.add_trace(go.Scatter(
#     x=df['Date'],
#     y=df["trace_-3"],
#     mode = 'lines',
#     name = '0.1%',
#     line = dict(width = 0.5, dash = 'dash', color = "red"),
#     fill='tonexty',
#     fillcolor='rgba(245, 66, 66,0.2)'  #Red
#     ))

# #Defines figure properties
# fig.update_layout(
#     title = coin_name + " uncertainity bands",
#     xaxis_title= "Date",
#     yaxis_title= coin_name + " price (USD)",
#     legend_title="Uncertainity risk levels",
    
#     plot_bgcolor = "black",
#     yaxis_type="log",
#     xaxis_rangeslider_visible=False)

# fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
# fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')

# st.plotly_chart(fig)
