import yfinance as yf


def get_stock_prices(ticker, period='max', interval='1wk', start=None, end=None):
    """
    Retrieves stock prices for a given ticker.
    :param end:
    :param start:
    :param ticker: stock ticker, e.g. 'AAPL'
    :param period: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
    :param interval: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'
    :return: stock prices
    """
    return yf.Ticker(ticker).history(period=period, interval=interval, start=start, end=end)