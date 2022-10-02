#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 5 00:34:10 2022

@author: stephandupoux
"""


from datetime import date, timedelta
import pandas as p
import requests
import time
import numpy as n


def upside_risk(stock_returns):
    ur = stock_returns[stock_returns > stock_returns.mean()].std(skipna = True) * n.sqrt(252)
    return ur

def downside_risk(stock_returns):
    dr = stock_returns[stock_returns < stock_returns.mean()].std(skipna = True) * n.sqrt(252)
    return dr

def daterange(start_date, end_date):
    for x in range(int((end_date - start_date).days)):
        yield start_date + timedelta(x)


#Y-M-D format. Change these dates to get the necessary query that you want. 
start_date = date(2020, 6, 1)
end_date = date(2020, 6, 10)
# Grab Currrent Time Before Running the Code




ETF = ['SPY', 'VIX']

metrics = []
start = time.time()
for i in ETF:
    data = []
    #Gets the data from polygon. 
    for single_date in daterange(start_date, end_date):
        update = single_date.strftime("%Y-%m-%d")
        response = requests.get(f'https://api.polygon.io/v1/open-close/{i}/{update}?adjusted=true&apiKey=el0FbXEICAXLDOh_2HHODn_QdqmBj_5WlhdNvp')
        responses = response.json()
        data.append(responses)
        print(update)
        
    #Turns it into a pandas dataframe
    df = p.DataFrame(data)
    # Filters for a specific ticker name and the ones that have no data for the dates
    df = df[df['symbol'] == i]
    # Drops unecessary columns
    df = df.drop(['request_id', 'message'], axis = 1)
    
    #This calculates the downside and upside for a ticker for Close price
    daily_close_pct_change = df['close'].pct_change().dropna()
    stock_ur_close = upside_risk(daily_close_pct_change)
    stock_dr_close = downside_risk(daily_close_pct_change)
    del daily_close_pct_change
    
    #This calculates the downside and upside for a ticker for Adjusted Close price
    daily_close_pct_change = df['afterHours'].pct_change().dropna()
    stock_ur_adj = upside_risk(daily_close_pct_change)
    stock_dr_adj = downside_risk(daily_close_pct_change)
    del daily_close_pct_change
    
    #Puts the data into a dictionary
    dpt = {'Ticker' : i, 'Downside Close' : stock_dr_close, 'Upside Close' : stock_ur_close,
           'Downside Adj' : stock_dr_adj, 'Upside Adj' : stock_ur_adj}
    
    #Stores it into a list
    metrics.append(dpt)
# Grab Currrent Time After Running the Code
end = time.time()
#Subtract Start Time from The End Time
total_time = end - start
print(f'Total Time is {str(total_time)}')

del df
df = p.DataFrame(metrics)

df.to_excel('Name it whatever.xlsx')


