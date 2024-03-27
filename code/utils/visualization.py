import matplotlib.pyplot as plt
import mplfinance as mpf


def plot_financial_chart(ticker, prices, chart_type='candle', sma_values=[]):
    """
    Plot the financial chart of a business entity.
    :param ticker: yfinance.Ticker object
    :param prices: pandas.DataFrame
    :param chart_type: 'line', 'candle', 'ohlc', 'renko', 'pnf', 'linebreak', 'kagi', 'heikinashi', 'hollowcandle'
    :param sma_values: list of integers representing the window sizes for SMAs
    """

    # implementation with yahoo finance api
    # prices.reset_index(inplace=True)
    # prices.plot(x='Date', y='Close', title=ticker.info['symbol'] + ' Stock Prices')
    # plt.show()

    data = prices[['Open', 'High', 'Low', 'Close']]

    # Calculate the SMAs and add them to the additional plots
    add_plots = []
    for sma in sma_values:
        sma_data = data['Close'].rolling(window=sma).mean()
        add_plots.append(mpf.make_addplot(sma_data))

    mpf.plot(data, type=chart_type, style='yahoo', title=ticker.info['symbol'] + ' Stock Prices', addplot=add_plots)
