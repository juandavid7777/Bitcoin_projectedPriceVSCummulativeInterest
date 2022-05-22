"""
Created on Wed Nov 17 09:19:21 2021
@author: Juan
"""
import pandas as pd
import numpy as np

import streamlit as strl

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import scipy.stats as st
from scipy.stats import norm


#1.-----Downloads data
df = pd.read_csv("https://raw.githubusercontent.com/juandavid7777/Bitcoin_projectedPriceVSCummulativeInterest/main/BTC_price_cummulative.csv", parse_dates = ["Date"])
df = df.set_index("Date", drop = False)

#2.-----API token definition
coin_name = "BTC"
projected_days = 180

#Inputs

    #Risk input
risk_select = strl.slider('Select your the risk level', 0.0, 1.0, 0.5, step = 0.01)
strl.write("Risk selected: ", risk_select*100, '%')

    #Date input
date_select = "2022-05-05"
date_select = strl.slider('Select date for forecast', "2011-01-01", "2025-05-05", "2022-05-05", step = 1)
strl.write("Date selected: ", date_select)

# Generates data
#Data resulting from analysis
B0, B1, B2, B3, SE_reg = [-3.358503319577917, 0.22504250770989914, -0.12935087625772632, 0.03602841985203026, 0.7339134037730446]



DSI_select = df.loc[date_select]["DSI"]
mean_price =  np.exp(B0 + B1*(np.log(DSI_select))**1 + B2*(np.log(DSI_select))**2 + B3*(np.log(DSI_select))**3)
risk_adj_price = np.exp(norm.ppf(risk_select, np.log(mean_price), SE_reg))

z_score = norm.ppf(risk_select)
df["line"] = np.exp(B0 + B1*(np.log(df["DSI"]))**1 + B2*(np.log(df["DSI"]))**2 + B3*(np.log(df["DSI"]))**3 + SE_reg*z_score)


#3.-----Plots figures
#=================================================== BANDS CHART===========================================
fig = go.Figure()

#Price candlesticks plots
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["close"],
    mode = 'lines',
    name = '',
    line = dict(width = 0.25, color = "white")
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
    y=df["trace_3"],
    mode = 'lines',
    name = '99.9%',
    line = dict(width = 0.5, dash = 'dash', color = "red"),
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_2"],
    mode = 'lines',
    name = '97.8%',
    line = dict(width = 0.5, dash = 'dash', color = "red"),
    fill='tonexty',
    fillcolor='rgba(245, 66, 66,0.5)'  #red
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_1"],
    mode = 'lines',
    name = '84.2%',
    line = dict(width = 0.5, dash = 'dash', color = "yellow"),\
    fill='tonexty',
    fillcolor='rgba(245, 66, 66,0.2)'  #red
    ))

#Prices regression plot
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_0"],
    mode = 'lines',
    name = '50.0%',
    line = dict(width = 1.0, dash = 'dash', color = "yellow"),
    fill='tonexty',
    fillcolor='rgba(245, 230, 66,0.5)'  #yellow
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_-1"],
    mode = 'lines',
    name = '15.8%',
    line = dict(width = 0.5, dash = 'dash', color = "yellow"),
    fill='tonexty',
    fillcolor='rgba(245, 230, 66,0.2)'  #yellow
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_-2"],
    mode = 'lines',
    name = '2.2%',
    line = dict(width = 0.5, dash = 'dash', color = "green"),
    fill='tonexty',
    fillcolor='rgba(0, 199, 56,0.2)'  #green
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_-3"],
    mode = 'lines',
    name = '0.1%',
    line = dict(width = 0.5, dash = 'dash', color = "green"),
    fill='tonexty',
    fillcolor='rgba(0, 199, 56,0.5)'  #green
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["line"],
    mode = 'lines',
    name = 'Selected risk',
    line = dict(width = 1.5, dash = 'solid', color = "silver"),
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

strl.plotly_chart(fig)
