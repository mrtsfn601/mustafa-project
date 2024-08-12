import yfinance as yf
from finvizfinance.quote import finvizfinance
from prettytable import PrettyTable


def discounted_cash_flow_formula(ticker_symbol):
    """
    Calculate the intrinsic value of a business using the Discounted Cash Flow (DCF) method.
    """
    yf_ticker = yf.Ticker(ticker_symbol)
    fv_ticker = finvizfinance(ticker_symbol)

    # Operating Cash Flow (Current TTM)
    operating_cash_flow_current = sum(
        yf_ticker.quarterly_cashflow.loc['Operating Cash Flow'].iloc[i] for i in range(4)) / 1_000_000

    # Liabilities
    current_debt = yf_ticker.quarterly_balance_sheet.loc['Current Debt'].iloc[0] / 1_000_000
    long_term_debt = yf_ticker.quarterly_balance_sheet.loc['Long Term Debt'].iloc[0] / 1_000_000
    debt = current_debt + long_term_debt

    # Assets
    cash = yf_ticker.quarterly_balance_sheet.loc['Cash Cash Equivalents And Short Term Investments'].iloc[0] / 1_000_000

    # Growth Rate
    cash_flow_1_5y = float(fv_ticker.ticker_fundament()['EPS next 5Y'].strip('%'))
    cash_flow_6_10y = min(cash_flow_1_5y, 15.00)
    cash_flow_10_20y = min(cash_flow_6_10y, 4.00)

    # Shares Outstanding
    shares_outstanding_str = fv_ticker.ticker_fundament()['Shs Outstand']  # 1.65B or 1.65M
    shares_outstanding = float(shares_outstanding_str[:-1])  # in millions
    if shares_outstanding_str[-1] == 'B':  # in billions
        shares_outstanding *= 1_000

    # Discount Rate for US Market
    risk_free_rate = 4.51  # source: http://www.market-risk-premia.com/us.html
    beta = float(fv_ticker.ticker_fundament()['Beta'])
    implied_market_risk_premium = 2.47  # source: http://www.market-risk-premia.com/us.html
    discount_rate = risk_free_rate + beta * implied_market_risk_premium
    discount_rate = 8.10  # %

    # Operating Cash Flow (Projected)
    operating_cash_flow_projected = operating_cash_flow_current
    discount_factor = 1
    discounted_cash_flow = 0
    # pre-calculate the cash flow growth rates for each year
    cash_flow_growth_rates = [cash_flow_1_5y] * 5 + [cash_flow_6_10y] * 5 + [cash_flow_10_20y] * 10

    for year in range(20):
        cash_flow_growth_rate = cash_flow_growth_rates[year]
        operating_cash_flow_projected *= (1 + cash_flow_growth_rate / 100)
        discount_factor /= (1 + discount_rate / 100)
        discounted_cash_flow += operating_cash_flow_projected * discount_factor

    # Intrinsic Value
    intrinsic_value = (discounted_cash_flow + cash - debt) / shares_outstanding

    # Share Price (Current)
    share_price = yf_ticker.history(period='1d')['Close'].iloc[0]

    # (Discount) or Premium
    discount = (intrinsic_value - share_price) / share_price * 100

    table = PrettyTable()
    table.title = f"${ticker_symbol} Intrinsic Value using Discounted Cash Flow"
    table.field_names = ["Metric", "Unit", "Value"]
    table.add_row(["Operating Cash Flow Current (TTM)", "$M", f"{operating_cash_flow_current:,.2f}"])
    table.add_row(["Current Debt (Quarter)", "$M", f"{current_debt:,.2f}"])
    table.add_row(["Long Term Debt (Quarter)", "$M", f"{long_term_debt:,.2f}"])
    table.add_row(["Total Debt (Quarter)", "$M", f"{debt:,.2f}"])
    table.add_row(["Cash, Cash Equivalents & Short Term Investments (Quarter)", "$M", f"{cash:,.2f}"])
    table.add_row(["Cash Flow Growth Rate   1-5 Years", "%", f"{cash_flow_1_5y:.2f}"])
    table.add_row(["Cash Flow Growth Rate  6-10 Years", "%", f"{cash_flow_6_10y:.2f}"])
    table.add_row(["Cash Flow Growth Rate 10-20 Years", "%", f"{cash_flow_10_20y:.2f}"])
    table.add_row(["Shares Outstanding", "M", f"{shares_outstanding:,.2f}"])
    table.add_row(["Discount Rate", "%", f"{discount_rate:.2f}"])
    table.add_row(["Operating Cash Flow Projected (20 Years)", "$M", f"{discounted_cash_flow:,.2f}"])
    table.add_row(["Intrinsic Value Per Share", "$", f"{intrinsic_value:.2f}"])
    table.add_row(["Share Price (Last Close)", "$", f"{share_price:.2f}"])
    table.align["Metric"] = "l"
    table.align["Value"] = "r"
    print(table)

    return table
