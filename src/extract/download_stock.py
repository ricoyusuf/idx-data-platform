import yfinance as yf 
import pandas as pd
ticker = "BBCA.JK"
stock_data = yf.download(ticker)
stock_data.columns = stock_data.columns.get_level_values(0)
print(type(stock_data))
print(stock_data.head())
print(stock_data.columns)
print(stock_data.info())

stock_data.reset_index().to_csv("data/BBCA.csv", index=False)