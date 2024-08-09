import yfinance as yf
from finvizfinance.quote import finvizfinance
from prettytable import PrettyTable


def discounted_cash_flow(ticker_symbol):
    """
    Calculate the intrinsic value of a business using the Discounted Cash Flow (DCF) method.
    """
    yf_ticker = yf.Ticker(ticker_symbol)
    fv_ticker = finvizfinance(ticker_symbol)

    operating_cash_flow_ttm = sum(
        yf_ticker.quarterly_cashflow.loc['Operating Cash Flow'].iloc[i] for i in range(4)) / 1_000_000

    short_term_debt = yf_ticker.quarterly_balance_sheet.loc['Current Debt'].iloc[0] / 1_000_000
    long_term_debt = yf_ticker.quarterly_balance_sheet.loc['Long Term Debt'].iloc[0] / 1_000_000
    total_debt = short_term_debt + long_term_debt

    cash = yf_ticker.quarterly_balance_sheet.loc['Cash Cash Equivalents And Short Term Investments'].iloc[0] / 1_000_000

    print(fv_ticker.ticker_fundament())
    cash_flow_1_5y = float(fv_ticker.ticker_fundament()['EPS next 5Y'].strip('%'))
    cash_flow_6_10y = min(cash_flow_1_5y, 15.00)
    cash_flow_10_20y = min(cash_flow_6_10y, 4.00)

    shares_outstanding_str = fv_ticker.ticker_fundament()['Shs Outstand']  # 1.65B or 1.65M
    shares_outstanding = float(shares_outstanding_str[:-1])  # in millions
    if shares_outstanding_str[-1] == 'B':  # in billions
        shares_outstanding *= 1_000

    table = PrettyTable()
    table.field_names = ["Metric", "Unit", "Value"]
    table.add_row(["Operating Cash Flow (TTM)", "$M", operating_cash_flow_ttm])
    table.add_row(["Short Term Debt (Quarter)", "$M", short_term_debt])
    table.add_row(["Long Term Debt (Quarter)", "$M", long_term_debt])
    table.add_row(["Total Debt (Quarter)", "$M", total_debt])
    table.add_row(["Cash, Cash Equivalents & Short Term Investments (Quarter)", "$M", cash])
    table.add_row(["Cash Flow Growth Rate   1-5 Years", "%", cash_flow_1_5y])
    table.add_row(["Cash Flow Growth Rate  6-10 Years", "%", cash_flow_6_10y])
    table.add_row(["Cash Flow Growth Rate 10-20 Years", "%", cash_flow_10_20y])
    table.add_row(["Shares Outstanding", "M", shares_outstanding])
    table.align["Metric"] = "l"
    table.align["Value"] = "r"
    print(table)

    return table
