"""
Created on Wed Nov 17 09:19:21 2021
@author: Juan
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime


#1.-----Downloads data
df = pd.read_csv("https://raw.githubusercontent.com/juandavid7777/BTC_risk_metric/891a1032cb63160763c33f235a4714f2083c9713/BTC_price_projections.csv")


#2.-----API token definition
coin_name = "BTC"
projected_days = 180


#3.-----Plots figures

#=================================================== BANDS CHART===========================================
fig = go.Figure()

#Price candlesticks plots
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["close"],
    mode = 'lines',
    name = '',
    line = dict(width = 0.5, color = "white")
    ))

fig.add_trace(go.Candlestick(
    x=df['Date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name = coin_name + ' price'
    ))

#Prices for uncertainity bands
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["plus_3STDV"],
    mode = 'lines',
    name = '99.9%',
    line = dict(width = 0.5, dash = 'dash', color = "red"),
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["plus_2STDV"],
    mode = 'lines',
    name = '97.8%',
    line = dict(width = 0.5, dash = 'dash', color = "yellow"),
    fill='tonexty',
    fillcolor='rgba(245, 66, 66,0.2)'  #Red
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["plus_1STDV"],
    mode = 'lines',
    name = '84.2%',
    line = dict(width = 0.5, dash = 'dash', color = "green"),\
    fill='tonexty',
    fillcolor='rgba(245, 230, 66,0.2)'  #yellow
    ))

#Prices regression plot
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["price_reg"],
    mode = 'lines',
    name = '50.0%',
    line = dict(width = 1.0, dash = 'dash', color = "grey"),
    fill='tonexty',
    fillcolor='rgba(0, 199, 56,0.2)'  #green
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["minus_1STDV"],
    mode = 'lines',
    name = '15.8%',
    line = dict(width = 0.5, dash = 'dash', color = "green"),
    fill='tonexty',
    fillcolor='rgba(0, 199, 56,0.2)'  #green
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["minus_2STDV"],
    mode = 'lines',
    name = '2.2%',
    line = dict(width = 0.5, dash = 'dash', color = "yellow"),
    fill='tonexty',
    fillcolor='rgba(245, 230, 66,0.2)'  #Yellow
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["minus_3STDV"],
    mode = 'lines',
    name = '0.1%',
    line = dict(width = 0.5, dash = 'dash', color = "red"),
    fill='tonexty',
    fillcolor='rgba(245, 66, 66,0.2)'  #Red
    ))

#Peaks
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["peak_price_plus_STDV"],
    mode = 'lines',
    name = 'Peak upper bound',
    line = dict(width = 0.5, dash = 'solid', color = "orange"),
    showlegend=False
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["peak_price_minus_STDV"],
    mode = 'lines',
    name = 'Peak lower bound',
    line = dict(width = 0.5, dash = 'solid', color = "orange"),
    fill='tonexty',
    fillcolor='rgba(245, 182, 66,0.5)',  #Red
    showlegend=False
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["peak_price"],
    mode = 'lines',
    name = 'Peak prediction',
    line = dict(width = 0.8, dash = 'dot', color = "orange"),
    showlegend=True
    ))

#Defines figure properties
fig.update_layout(
    title = coin_name + " uncertainity bands",
    xaxis_title= "Date",
    yaxis_title= coin_name + " price (USD)",
    legend_title="Uncertainity risk levels",
    
    plot_bgcolor = "black",
    yaxis_type="log",
    xaxis_rangeslider_visible=False)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')

st.plotly_chart(fig)


#===================COLORED CHART=====================================

fig = go.Figure()

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["close"],
    mode = 'markers',
    name = '',
    marker=dict(size=3,color = df["norm_dist"], colorscale='Jet',showscale=True)
    ),secondary_y=False)

#Defines figure properties
fig.update_layout(
    title = coin_name + " uncertainity colored metric",
    xaxis_title= "Date",
    yaxis_title= coin_name + " price (USD)",
    
    plot_bgcolor = "black",
    yaxis_type="log",
    xaxis_rangeslider_visible=False)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')

st.plotly_chart(fig)

#======================== Risk metric chart ========================================

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["close"],
    mode = 'lines',
    name = 'Price',
    line = dict(width = 2.0, color = "white")
    ),secondary_y=False)

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["norm_dist"],
    mode = 'lines',
    name = 'Risk metric',
    line = dict(width = 1.0, color = "orange")
    ),secondary_y=True)

#Defines figure properties
fig.update_layout(
    title = coin_name + " uncertainity metric",
    xaxis_title= "Date",
    yaxis_title= coin_name + " price (USD)",
    
    plot_bgcolor = "black",
    yaxis_type="log",
    xaxis_rangeslider_visible=False)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey', secondary_y = False)
fig.update_yaxes(title = "Risk metric (0 - 1)", showgrid=True, gridwidth=1, gridcolor='pink', secondary_y = True)

st.plotly_chart(fig)
