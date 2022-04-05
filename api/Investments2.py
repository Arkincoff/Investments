import numpy as np
import pandas as pd
import yfinance as yf
from flask_cors import CORS
import requests
from flask import Flask, request, jsonify
import requests
from lxml import html
import json

app = Flask(__name__)
CORS(app)


@app.route("/")
def Investments():
    extra_rows = 2
    each_market_rows = 5

    df = pd.read_excel (r'Investments.xlsx','Sayfa2')
    number_of_markets = int ((len(df.index)-extra_rows)/each_market_rows)
    markets = []
    values = []*number_of_markets
    prices = []*number_of_markets
    coins_in_market = []*number_of_markets
    costs = []*number_of_markets
    amounts = []*number_of_markets
    gain_loss = []*number_of_markets
    total_costs = []
    total_values = []
    results = ""
    for i in range(number_of_markets):
        markets = markets + [str(df.iloc[5*i,0])]
    for i in range(number_of_markets):
        temp_coins = []
        temp_costs = []
        temp_amounts = []
        for j in range(len(df.columns)-1):
            if df.iloc[5*i+1,j+1] != 0:
                temp_coins = temp_coins + [df.iloc[5*i,j+1]]
                temp_costs = temp_costs + [df.iloc[5*i+3,j+1]]
                temp_amounts = temp_amounts + [df.iloc[5*i+1,j+1]]
        coins_in_market = coins_in_market + [temp_coins]
        costs = costs + [temp_costs]
        amounts = amounts + [temp_amounts]
    for i in range(number_of_markets):
        temp_values = []
        temp_prices = []
        price = 0
        if len(coins_in_market[i]) > 1:
            for j in range(len(coins_in_market[i])):
                url = 'https://coinmarketcap.com/currencies/' +  coins_in_market[i][j] +'/'
                page = requests.get(url)
                tree = html.fromstring(page.content)
                value = (tree.xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span/text()'))
                res = [i for i, val in enumerate(df.iloc[5*i,:] == coins_in_market[i][j]) if val][0]
                if not value:
                    value = tree.xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/div/span/text()')
                    res = [i for i, val in enumerate(df.iloc[5*i,:] == coins_in_market[i][j]) if val][0]
                price = float ((str(value[0])[1:]).replace(",",""))
                temp_prices = temp_prices + [price]
                temp_values = temp_values + [price*df.iloc[5*i+1,res]]
            values = values + [temp_values]
            prices = prices + [temp_prices]
        else:
            url = 'https://coinmarketcap.com/currencies/' +  coins_in_market[i][0] +'/'
            page = requests.get(url)
            tree = html.fromstring(page.content)
            value = (tree.xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span/text()'))
            res = [i for i, val in enumerate(df.iloc[5*i,:] == coins_in_market[i][0]) if val][0]
            if not value:
                value = tree.xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/div/span/text()')
                res = [i for i, val in enumerate(df.iloc[5*i,:] == coins_in_market[i]) if val][0]
            price = float ((str(value[0])[1:]).replace(",",""))
            temp_prices = temp_prices + [price]
            temp_values = temp_values + [price*df.iloc[5*i+1,res]]
            values = values + [temp_values]
            prices = prices + [temp_prices]
    for i in range(number_of_markets):
        total_costs = total_costs + [sum(costs[i])]
        total_values = total_values + [sum(values[i])]
    overall_cost = sum(total_costs)
    overall_value = sum(total_values)
    for i in range(number_of_markets):
        temp_gain_loss = []
        if len(coins_in_market[i]) > 1:
            for j in range(len(coins_in_market[i])):
                temp_gain_loss = temp_gain_loss + [100*(values[i][j] - costs[i][j])/costs[i][j]]
        else:
            temp_gain_loss = temp_gain_loss + [100*(values[i][0] - costs[i][0])/costs[i][0]]
        gain_loss = gain_loss + [temp_gain_loss]
            
    for i in range(number_of_markets):
        if len(coins_in_market[i]) > 1:
            for j in range(len(coins_in_market[i])):
                results = results + coins_in_market[i][j] + ":<br />\nAmount: " + str(amounts[i][j]) + "<br />\nPrice: " + str(prices[i][j]) + "<br />\nCost: " + str(costs[i][j]) + "<br />\nCurrent Value: " + str(values[i][j]) + "<br />\nProfit/Loss: " + str(gain_loss[i][j]) +"<br />\n<br />\n"
        else:
            results = results + coins_in_market[i][0] + ":<br />\nAmount: " + str(amounts[i][0]) + "<br />\nPrice: " + str(prices[i][0]) + "<br />\nCost: " + str(costs[i][0]) + "<br />\nCurrent Value: " + str(values[i][0]) + "<br />\nProfit/Loss: " + str(gain_loss[i][0]) + "<br />\n<br />\n"
    for i in range(number_of_markets):
        results = results + "<br />\n" + markets[i] + ":<br />\n" + "total costs: " + str(total_costs[i]) + "<br />\n" + "total values: " + str(total_values[i]) + "<br />\n<br />\n"
    results = results + "overall cost: " + str(overall_cost) + "<br />\n" + "overall value: " + str(overall_value) + "<br />\n"
    return results

if __name__ == "__main__":
    app.run(host='0.0.0.0')

