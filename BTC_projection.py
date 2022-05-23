"""
Created on Wed Nov 17 09:19:21 2021
@author: Juan
"""
#Imports packages
import pandas as pd
import numpy as np

import streamlit as strl

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import scipy.stats as st
from scipy.stats import norm

from datetime import datetime

import webcolors

#0 Functions
    #Color function
def css_to_rgb(color_name, opacity):
    r,g,b = webcolors.name_to_rgb(color_name)
    
    return "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(opacity)+")"


#1. Downloads data
df = pd.read_csv("https://raw.githubusercontent.com/juandavid7777/Bitcoin_projectedPriceVSCummulativeInterest/main/BTC_price_cummulative.csv", parse_dates = ["Date"])
df = df.set_index("Date", drop = False)

#2. Coin name
coin_name = "BTC"

#3. User inputs

    #Risk input
risk_select = strl.sidebar.slider('Select your the risk level', 0.01, 0.99, 0.5, step = 0.01)
strl.sidebar.write("Risk selected: ", risk_select*100, '%')

    #Date input
date_select = strl.sidebar.slider(
     "When do you forecast the price?",
     min_value = datetime(2011, 1, 1),
     max_value = datetime(2025, 5, 5),
     value = datetime(2022, 5, 5),
     format="YYYY-MM-DD")
strl.sidebar.write("Date Analysis:", date_select)


#4.Data analysis
    #Data resulting from analysis
B0, B1, B2, B3, SE_reg = [-3.358503319577917, 0.22504250770989914, -0.12935087625772632, 0.03602841985203026, 0.7339134037730446]

    #Estimates points
DSI_select = df.loc[date_select]["DSI"]
mean_price =  np.exp(B0 + B1*(np.log(DSI_select))**1 + B2*(np.log(DSI_select))**2 + B3*(np.log(DSI_select))**3)
risk_adj_price = np.exp(norm.ppf(risk_select, np.log(mean_price), SE_reg))

z_score = norm.ppf(risk_select)
df["line"] = np.exp(B0 + B1*(np.log(df["DSI"]))**1 + B2*(np.log(df["DSI"]))**2 + B3*(np.log(df["DSI"]))**3 + SE_reg*z_score)

strl.write("---------------------------------------------------------------------------------------------------------------")
strl.write("Forecasted price:", risk_adj_price)

#5.Plots figures
fig = go.Figure()

    #Prices for uncertainity bands
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_3"],
    mode = 'lines',
    name = '99.9%',
    line = dict(width = 0.2, dash = 'dash', color = "red"),
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_2"],
    mode = 'lines',
    name = '97.8%',
    line = dict(width = 0.2, dash = 'dash', color = "red"),
    fill='tonexty',
    fillcolor= css_to_rgb("tomato", 0.2)  #red
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_1"],
    mode = 'lines',
    name = '84.2%',
    line = dict(width = 0.2, dash = 'dash', color = "yellow"),\
    fill='tonexty',
    fillcolor=css_to_rgb("salmon", 0.2)  #red
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_0"],
    mode = 'lines',
    name = '50.0%',
    line = dict(width = 0.2, dash = 'dash', color = "yellow"),
    fill='tonexty',
    fillcolor=css_to_rgb("khaki", 0.2)  #yellow
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_-1"],
    mode = 'lines',
    name = '15.8%',
    line = dict(width = 0.2, dash = 'dash', color = "yellow"),
    fill='tonexty',
    fillcolor=css_to_rgb("lemonchiffon", 0.2) #yellow
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_-2"],
    mode = 'lines',
    name = '2.2%',
    line = dict(width = 0.2, dash = 'dash', color = "green"),
    fill='tonexty',
    fillcolor=css_to_rgb("palegreen", 0.2) #green
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["trace_-3"],
    mode = 'lines',
    name = '0.1%',
    line = dict(width = 0.2, dash = 'dash', color = "green"),
    fill='tonexty',
    fillcolor=css_to_rgb("lawngreen", 0.2)  #green
    ))

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df["line"],
    mode = 'lines',
    name = "Selected risk: " + str(risk_select*100) + "%",
    line = dict(width = 1.5, dash = 'solid', color = "cyan"),
    ))

fig.add_vline(x=date_select, line_width=1.5, line_dash="solid", line_color="cyan")

    #Price candlesticks plots
fig.add_trace(go.Candlestick(
    x=df['Date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name = coin_name + ' price'
    ))

    #Defines figure properties
fig.update_layout(
    title = coin_name + " price-risk bands",
    xaxis_title= "Date",
    yaxis_title= coin_name + " price (USD)",
    legend_title="Uncertainity price-risk levels",
    
    plot_bgcolor = "black",
    yaxis_type="log",
    xaxis_rangeslider_visible=False)
    
    #Sets up grid and axis properties
fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='dimgrey')
fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='dimgrey')
fig.update_layout(hovermode="x")

strl.plotly_chart(fig)
