import matplotlib.pyplot as plt
from pprint import pprint
import yfinance as yf

import utils.financials as fin

ticker_symbol = 'AAPL'
ticker = yf.Ticker(ticker_symbol)

"""
:param period: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
:param interval: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'
:param start: start date, e.g. '2021-01-01'
:param end: end date, e.g. '2024-02-28'
"""
prices = ticker.history(period='max', interval='1mo')

prices.reset_index(inplace=True)
prices.plot(x='Date', y='Close', title=ticker_symbol + ' Stock Prices')
plt.show()

operating_cash_flow = fin.get_operating_cash_flow(ticker, annual=True).iloc[0]
print(f'The operating cash flow for {ticker_symbol} is {operating_cash_flow}')

# pprint(ticker.info)
# print(ticker.actions)  # actions (dividends and splits)
# print(ticker.dividends)
# print(ticker.splits)
# print(ticker.financials)
# print(ticker.balance_sheet)
# print(ticker.cashflow)
# print(ticker.get_sustainability())
# print(ticker.recommendations)
# print(ticker.calendar)
# print(ticker.isin)
# print(ticker.options)
# print(ticker.option_chain('2024-01-20'))  # replace with a valid expiry date
