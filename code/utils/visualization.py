import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf


def plot_financial_chart(ticker_symbol, period='10y', interval='1wk', start=None, end=None, chart_type='candle',
                         sma_values=[50, 100, 150, 200]):
    """
    Plot the financial chart of a business entity.
    :param ticker_symbol: the stock ticker symbol
    :param period: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
    :param interval: '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'
    :param start: start date, e.g. '2021-01-01'
    :param end: end date, e.g. '2024-02-28'
    :param chart_type: 'line', 'candle', 'ohlc', 'renko', 'pnf', 'linebreak', 'kagi', 'heikinashi', 'hollowcandle'
    :param sma_values: list of integers representing the window sizes for SMAs
    """
    ticker = yf.Ticker(ticker_symbol)
    prices = ticker.history(period=period, interval=interval, start=start, end=end)

    # option #1: plot with yahoo finance api
    # prices.reset_index(inplace=True)
    # prices.plot(x='Date', y='Close', title=ticker.info['symbol'] + ' Stock Prices')
    # plt.show()

    # option #2: plot with mplfinance
    data = prices[['Open', 'High', 'Low', 'Close']]
    # Calculate the SMAs and add them to the additional plots
    add_plots = []
    for sma in sma_values:
        sma_data = data['Close'].rolling(window=sma).mean()
        add_plots.append(mpf.make_addplot(sma_data))
    mpf.plot(data, type=chart_type, style='yahoo', title=ticker.info['symbol'] + ' Stock Prices', addplot=add_plots)


def plot_operating_cash_flow(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    operating_cash_flow = ticker.cashflow.loc['Operating Cash Flow']
    print(operating_cash_flow)
    # operating_cash_flow.plot(title=f"{ticker_symbol} Operating Cash Flow")
    # plt.show()