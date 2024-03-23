def get_operating_cash_flow(ticker, annual=True):
    """
    Get the operating cash flow of a business entity from its financials data.
    :param ticker: yfinance.Ticker object
    :param annual: bool, default True (for annual data) or False (for quarterly data)
    :return: pandas.Series or None
    """
    cashflow = ticker.cashflow if annual else ticker.quarterly_cashflow
    try:
        return cashflow.loc['Operating Cash Flow']
    except KeyError:
        return None
