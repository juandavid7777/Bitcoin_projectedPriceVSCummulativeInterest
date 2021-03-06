"""
Created on May 15 09:19:21 2022
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
from datetime import date

import requests

#0 Functions
from functions import css_to_rgb

#1. Downloads data
df = pd.read_csv("https://raw.githubusercontent.com/juandavid7777/Bitcoin_projectedPriceVSCummulativeInterest/main/BTC_price_cummulative.csv", parse_dates = ["Date"])
df = df.set_index("Date", drop = False)

#2. Coin name and latest price
coin_name = "BTC"
    
    #API latest price
base_url = "https://api.coingecko.com/api/v3"
url = base_url + f"/simple/price?ids=bitcoin&vs_currencies=usd"
r = requests.get(url)
last_price = r.json()['bitcoin']['usd']

#3. User inputs in a side bar

    #Image gears
strl.sidebar.image("gears.png")

    #Risk input
risk_select = strl.sidebar.slider('Risk level', 0.01, 0.99, 0.5, step = 0.05)

    #Date input
date_select = strl.sidebar.slider(
     "Cash out date",
     min_value = datetime(2011, 1, 1),
     max_value = datetime(2032, 5, 5),
     value = datetime(2024, 5, 5),
     format="YYYY-MM-DD")

date_select_d = date_select.date()

    #BTC input
BTCin = strl.sidebar.slider('BTC initial capital (BTC)', 0.01, 50.0, 10.0, step = 1.0)

    #BTC earning rate
BTCr = strl.sidebar.slider('BTC earnings APY (%)', 0.0, 25.0, 5.0, step = 0.5)/100
BTCr_daily = (1+BTCr )**(1/365)-1

#4.Data analysis

    #Data resulting from analysis
B0, B1, B2, B3, SE_reg = [-3.358503319577917, 0.22504250770989914, -0.12935087625772632, 0.03602841985203026, 0.7339134037730446]

    #Estimates points
DSI_select = df.loc[date_select]["DSI"]

    #fitler max data
DSI_filter = DSI_select + 365
df = df[df["DSI"] < DSI_filter]

mean_price =  np.exp(B0 + B1*(np.log(DSI_select))**1 + B2*(np.log(DSI_select))**2 + B3*(np.log(DSI_select))**3)
risk_adj_price = np.exp(norm.ppf(risk_select, np.log(mean_price), SE_reg))

    #Current risk
price = np.log(last_price)
mean = np.log(df["50.00%"].loc[df["close"].last_valid_index()])
current_percent = norm.cdf(price, mean, SE_reg)    

z_score = norm.ppf(risk_select)
df["line"] = np.exp(B0 + B1*(np.log(df["DSI"]))**1 + B2*(np.log(df["DSI"]))**2 + B3*(np.log(df["DSI"]))**3 + SE_reg*z_score)

    #Compounded analysis for daily equivalent
today_date = date.today()
n_days = (date_select_d - today_date).days
n_years = n_days/365
BTCout = BTCin*(1+BTCr_daily)**n_days

    #Investment analysis
HOLD_gains = (risk_adj_price-last_price)/last_price*100
acc_HOLD_gains = (risk_adj_price*BTCout-last_price*BTCin)/(last_price*BTCin)*100

#5. Prints
    #Image
strl.image("bitcoin.jpg")

    #Title
strl.markdown('<b style="color:darkgoldenrod ; font-size: 44px">Bitcoin logarithmic investment projections</b>', unsafe_allow_html=True)

    #Creates triple column
col1, col2, col3 = strl.columns(3)

with col1:
    strl.header("Risk taken")

    #Model assumptions
    strl.write("Risk selected: ", risk_select*100, '%')
    strl.write("Bitcoin earnings/year: ", BTCr*100, '%')
    strl.write("Today's risk: ", float("{:.2f}".format(current_percent*100)), '%')

with col2:
    strl.header("Buy Bitcoin today")
    
    #Selected inputs
    strl.write("Bitcoin bought: ", BTCin, 'BTC')
    strl.write("Present BTC price: ", last_price, 'USD/BTC')
    
with col3:
    strl.header("Cash out on: " +  str(date_select_d))

    #resulting outputs
    strl.write("Bitcoin accumulated: ", float("{:.2f}".format(BTCout)), 'BTC')
    strl.write("Future BTC price:", float("{:.0f}".format(risk_adj_price)), "USD/BTC")
   
    #Investment analysis
strl.write("---------------------------------------------------------------------------------------------------------------")
strl.header("Investment Analysis")

    #Summary table creation
params = ["Present investment value (USD)" ,"BTC accumulated","Future investment value (USD)","Total gains (%)","Yearly ROI (%)"]
hold_strat = [BTCin*last_price,BTCin,BTCin*risk_adj_price,HOLD_gains,HOLD_gains/n_years]
earn_strat = [BTCin*last_price,BTCout,BTCout*risk_adj_price,acc_HOLD_gains,acc_HOLD_gains/n_years]

data = {"HODL":hold_strat, "HODL + earn":earn_strat }
df_sum = pd.DataFrame(data = data, index = params)

strl.table(df_sum)

#6.Plots figures

fig = go.Figure()

risks = ["99.90%", "90.00%", "80.00%", "70.00%", "60.00%", "50.00%", "40.00%", "30.00%", "20.00%", "10.00%", "0.10%"]

for risk_name in risks:
        #Prices for uncertainity bands
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df[risk_name],
        mode = 'lines',
        name = risk_name,
        line = dict(width = 0.2, dash = 'dash', color = "black"),
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
    
    plot_bgcolor = "ghostwhite",
    yaxis_type="log",
    xaxis_rangeslider_visible=False)
    
    #Sets up grid and axis properties
fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='dimgrey')
fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='dimgrey')
fig.update_layout(hovermode="x unified")

strl.plotly_chart(fig)

# 7. Footer
strl.write("------------------------------------------------------")
strl.write("Bitcoin Price Prediction: Using This Tool")
strl.caption("Assuming Bitcoin continues to be adopted over time, this chart can be used as a price prediction tool where there is potential for price movement between the upper and lower boundaries as support and resistance. These levels are estimated according to the price deviations from the logarithmic growth trend of BTC across all its history. The price levels corresponding to each risk level can be seen by hovering over the graph, and can be understood as the price deviation uncertainity from the long term growth trend. As a hint, the best buying points happened below the 20% risk level and peaks have always occurred above the 90% level. Because the curves can be calculated on a forward-looking basis, it is possible to forecast where the price of Bitcoin may move towards in the future. Have fun speculating!")
strl.caption("Inspired by Cole Garner (@quantadelic) and the article from Harold Christopher Burger (@hcburguer): Bitcoin's natural long-term power corridor of growth [link](https://medium.com/quantodian-publications/bitcoins-natural-long-term-power-law-corridor-of-growth-649d0e9b3c94)")