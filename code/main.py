from pprint import pprint
import utils.intrinsic_value as iv
import utils.sp500 as sp500
import utils.visualization as vis
import yfinance as yf

ticker_symbol = 'AMZN'
tickers = [ticker_symbol]
# tickers = ['AAPL', 'ADAP', 'AMZN', 'AZN', 'CRM', 'GOOGL', 'JNJ', 'MA', 'MCD', 'META', 'MSFT', 'NKE', 'NVDA', 'PEP', 'TSLA', 'UNH']
# tickers = sp500.sp500_tickers()

# Calculate Intrinsic Value using Discounted Cash Flow (DCF) method
for ticker_symbol in tickers:
    iv.discounted_cash_flow_formula(ticker_symbol, years=20, filter_out=True)

# Print the chart price of the stock
# vis.plot_financial_chart(ticker_symbol)

ticker = yf.Ticker(ticker_symbol)
# pprint(ticker.info)
# print(ticker.actions)  # actions (dividends and splits)
# print(ticker.dividends)
# print(ticker.splits)
# print(ticker.financials)
# print(ticker.earnings)
# print(ticker.balance_sheet)
# print(ticker.cashflow)
# print(ticker.get_sustainability())
# print(ticker.recommendations)
# print(ticker.calendar)
# print(ticker.isin)
# print(ticker.options)
# print(ticker.option_chain('2024-01-20'))  # replace with a valid expiry date
