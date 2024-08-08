from prettytable import PrettyTable


def discounted_cash_flow(ticker):
    """
    Calculate the intrinsic value of a business entity using the Discounted Cash Flow (DCF) method.
    :param ticker: yfinance.Ticker object
    """
    # todo get TTM operating cash flow value
    operating_cash_flow = ticker.cashflow.loc['Operating Cash Flow'].iloc[0] / 1_000_000

    short_term_debt = ticker.quarterly_balance_sheet.loc['Current Debt'].iloc[0] / 1_000_000 # in millions
    long_term_debt = ticker.quarterly_balance_sheet.loc['Long Term Debt'].iloc[0] / 1_000_000 # in millions
    total_debt = short_term_debt + long_term_debt

    table = PrettyTable()
    table.field_names = ["Metric", "Value"]
    table.add_row(["Operating Cash Flow (Annual TTM, $ in millions)", operating_cash_flow])
    table.add_row(["Short Term Debt (Quarterly, $ in millions)", short_term_debt])
    table.add_row(["Long Term Debt (Quarterly, $ in millions)", long_term_debt])
    table.add_row(["Total Debt (Quarterly, $ in millions)", total_debt])
    table.align["Metric"] = "l"
    table.align["Value"] = "r"
    print(table)

    # cash_flow = ticker.cashflow.loc['Total Cash From Operating Activities'].iloc[0]
    # growth_rate = get_growth_rate(ticker, years)
    # discount_rate = get_discount_rate(ticker)
    # dcf = sum([cash_flow * (1 + growth_rate) ** year / (1 + discount_rate) ** year for year in range(1, years + 1)])
    # shares_outstanding = ticker.info['sharesOutstanding']
    # intrinsic_value = dcf / shares_outstanding
    # return intrinsic_value
    return 1