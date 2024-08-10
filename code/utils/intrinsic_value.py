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

    cash_flow_1_5y = float(fv_ticker.ticker_fundament()['EPS next 5Y'].strip('%'))
    cash_flow_6_10y = min(cash_flow_1_5y, 15.00)
    cash_flow_10_20y = min(cash_flow_6_10y, 4.00)

    shares_outstanding_str = fv_ticker.ticker_fundament()['Shs Outstand']  # 1.65B or 1.65M
    shares_outstanding = float(shares_outstanding_str[:-1])  # in millions
    if shares_outstanding_str[-1] == 'B':  # in billions
        shares_outstanding *= 1_000

    beta = float(fv_ticker.ticker_fundament()['Beta'])
    discount_rate = 5.2
    if 0.8 < beta <= 1.0:
        discount_rate = 5.9
    elif 1.0 < beta <= 1.1:
        discount_rate = 6.3
    elif 1.1 < beta <= 1.2:
        discount_rate = 6.6
    elif 1.2 < beta <= 1.3:
        discount_rate = 7.0
    elif 1.3 < beta <= 1.4:
        discount_rate = 7.4
    elif 1.4 < beta <= 1.5:
        discount_rate = 7.7
    elif 1.5 < beta:
        discount_rate = 8.1

    table = PrettyTable()
    table.title = f"${ticker_symbol} Intrinsic Value using Discounted Cash Flow"
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
    table.add_row(["Discount Rate", "%", discount_rate])
    table.align["Metric"] = "l"
    table.align["Value"] = "r"
    print(table)

    return table
