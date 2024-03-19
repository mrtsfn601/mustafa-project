import matplotlib.pyplot as plt
from stockprice import get_stock_prices
import yfinance as yf


prices = get_stock_prices("AAPL", period='1y', interval='1d', start='2021-01-01', end='2024-02-28')
# print(prices)

prices.reset_index(inplace=True)
prices.plot(x='Date', y='Close', title='AAPL Stock Prices')
plt.show()


ticker = yf.Ticker("AAPL")
# print(ticker.info)
# print(ticker.actions)  # actions (dividends and splits)
# print(ticker.dividends)
# print(ticker.splits)
# print(ticker.financials)
# print(ticker.balance_sheet)
# print(ticker.cashflow)
# print(ticker.sustainability)
# print(ticker.recommendations)
# print(ticker.calendar)
# print(ticker.isin)
# print(ticker.options)
# print(ticker.option_chain('2024-01-20'))  # replace with a valid expiry date
