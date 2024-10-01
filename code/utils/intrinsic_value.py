import pandas as pd
import yfinance as yf
from finvizfinance.quote import finvizfinance
from prettytable import PrettyTable
from colorama import Fore, Style


def discounted_cash_flow_formula(ticker_symbol, years=20, filter_out=True):
    """
    Calculate the intrinsic value of a business using the Discounted Cash Flow (DCF) method.
    :param ticker_symbol: the stock ticker symbol
    :param years: the number of years to calculate the intrinsic value over, max 20 years
    :param filter_out: filter out stocks that are not growing consistently
    Implementation notes:
    - $ amounts are converted to millions.
    """
    print(ticker_symbol)
    yf_ticker = yf.Ticker(ticker_symbol)
    try:
        fv_ticker = finvizfinance(ticker_symbol)  # BRK.B
    except Exception as e:
        print(f"Error occurred {e} with {ticker_symbol}.")
        ticker_symbol = ticker_symbol.replace('.', '-')
        try:
            fv_ticker = finvizfinance(ticker_symbol)  # BRK-B
        except Exception as e:
            print(f"Error occurred again: {e}. Unable to fetch data for ticker symbol {ticker_symbol}.")
            return

    # if country is not USA, skip
    if filter_out and fv_ticker.ticker_fundament()['Country'] != 'USA':
        print(f"Skipping {ticker_symbol} due to country.")
        return

    # if business is not in the given list of sectors, skip
    good_sectors = ['Communication Services', 'Consumer Cyclical', 'Consumer Defensive', 'Technology', 'Healthcare']
    sector = fv_ticker.ticker_fundament()['Sector']
    if filter_out and sector not in good_sectors:
        print(f"Skipping {ticker_symbol} due to {sector} sector.")
        return

    # if business is in the given list of industries, skip
    bad_industries = ['Auto Parts', 'Entertainment']
    if filter_out and fv_ticker.ticker_fundament()['Industry'] in bad_industries:
        print(f"Skipping {ticker_symbol} due to industry.")
        return

    # Operating Cash Flow (Current TTM)
    operating_cash_flow_current = sum(
        get(yf_ticker.quarterly_cashflow, 'Operating Cash Flow', i) for i in range(4)) / 1_000_000

    # Liabilities
    current_debt = get(yf_ticker.quarterly_balance_sheet, 'Current Debt') / 1_000_000
    long_term_debt = get(yf_ticker.quarterly_balance_sheet, 'Long Term Debt') / 1_000_000
    debt = current_debt + long_term_debt

    # Assets
    cash = get(yf_ticker.quarterly_balance_sheet, 'Cash Cash Equivalents And Short Term Investments') / 1_000_000

    # Growth Rates: 1-5 Years, 6-10 Years, 10-20 Years
    try:
        cash_flow_1_5y = float(fv_ticker.ticker_fundament()['EPS next 5Y'].strip('%'))
    except ValueError:
        print(f"'EPS next 5Y' not found for {ticker_symbol}. Setting value to 0.")
        cash_flow_1_5y = 0.0
    cash_flow_6_10y = min(cash_flow_1_5y, 15.00)
    cash_flow_10_20y = min(cash_flow_6_10y, 4.00)

    # if growth rate is less than criteria, skip
    if filter_out and cash_flow_1_5y < 10:
        print(f"Skipping {ticker_symbol} due to low {cash_flow_1_5y:.2f}% growth rate (EPS next 5Y).")
        return

    # Shares Outstanding
    shares_outstanding_str = fv_ticker.ticker_fundament()['Shs Outstand']  # ex: 1.65M, 1.65B
    shares_outstanding = float(shares_outstanding_str[:-1])  # in millions
    if shares_outstanding_str[-1] == 'B':  # if in billions
        shares_outstanding *= 1_000  # convert to millions

    # Discount Rate for US Market
    risk_free_rate = 4.09  # source: http://www.market-risk-premia.com/us.html
    beta = float(fv_ticker.ticker_fundament()['Beta'])
    implied_market_risk_premium = 2.51  # source: http://www.market-risk-premia.com/us.html
    discount_rate = risk_free_rate + beta * implied_market_risk_premium

    # Operating Cash Flow (Projected)
    operating_cash_flow_projected = operating_cash_flow_current
    discount_factor = 1
    discounted_cash_flow = 0
    # pre-calculate the cash flow growth rates for each year
    cash_flow_growth_rates = [cash_flow_1_5y] * 5 + [cash_flow_6_10y] * 5 + [cash_flow_10_20y] * 10

    for year in range(years):
        cash_flow_growth_rate = cash_flow_growth_rates[year]
        operating_cash_flow_projected *= (1 + cash_flow_growth_rate / 100)
        discount_factor /= (1 + discount_rate / 100)
        discounted_cash_flow += operating_cash_flow_projected * discount_factor

    # Intrinsic Value vs Share Price (Current)
    intrinsic_value = (discounted_cash_flow + cash - debt) / shares_outstanding
    try:
        share_price = yf_ticker.history(period='1d')['Close'].iloc[0]
    except IndexError:
        print(f"No closing price data available for ticker symbol {ticker_symbol}.")
        return
    share_price_diff_abs = share_price - intrinsic_value  # $ amount
    share_price_diff_rel = share_price_diff_abs / share_price * 100  # % amount
    is_overpriced = share_price > intrinsic_value

    # if share price is not discounted, skip
    if filter_out and -20 < share_price_diff_rel:
        print(f"Skipping {ticker_symbol} due to low {share_price_diff_rel:.2f}% discount.")
        return

    # Where is the share price in relation to the SMAs
    try:
        share_price_history = yf_ticker.history(period='5y', interval='1d')['Close']
    except IndexError:
        share_price_history = yf_ticker.history(period='max', interval='1d')['Close']
    sma_50 = share_price_history.rolling(window=50).mean().iloc[-1]
    sma_100 = share_price_history.rolling(window=100).mean().iloc[-1]
    sma_150 = share_price_history.rolling(window=150).mean().iloc[-1]
    sma_200 = share_price_history.rolling(window=200).mean().iloc[-1]

    # if share price is above 50 SMA, skip
    if filter_out and share_price > sma_50:
        print(f"Skipping {ticker_symbol} due to being above 50 SMA.")
        return

    table = PrettyTable()
    table.title = f"${ticker_symbol} Intrinsic Value using Discounted Cash Flow"
    table.field_names = ["Metric", "Value", "Unit"]
    table.add_row(["Operating Cash Flow Current (TTM)", f"{operating_cash_flow_current:,.2f}", "$M"])
    table.add_row(["Debt: Current Debt & Long Term Debt (Quarter)", f"{debt:,.2f}", "$M"])
    table.add_row(["Cash, Cash Equivalents & Short Term Investments (Quarter)", f"{cash:,.2f}", "$M"])
    table.add_row(["Cash Flow Growth Rate   1-5 Years", f"{cash_flow_1_5y:.2f}", "%"])
    table.add_row(["Cash Flow Growth Rate  6-10 Years", f"{cash_flow_6_10y:.2f}", "%"])
    table.add_row(["Cash Flow Growth Rate 10-20 Years", f"{cash_flow_10_20y:.2f}", "%"])
    table.add_row(["Shares Outstanding", f"{shares_outstanding:,.2f}", "M"])
    table.add_row(["Discount Rate", f"{discount_rate:.2f}", "%"])
    table.add_row([f"Operating Cash Flow Projected ({years} Years)", f"{discounted_cash_flow:,.2f}", "$M"])
    table.add_row(["Share Price (Last Close)", f"{share_price:.2f}", "$"])
    table.add_row([decor(is_overpriced, "Intrinsic Value"), f"{intrinsic_value:.2f}", "$"])
    table.add_row([decor(is_overpriced, "Overpriced", "Underpriced"), f"{share_price_diff_abs:.2f}", "$"])
    table.add_row([decor(is_overpriced, "Premium", "Discount"), f"{share_price_diff_rel:.2f}", "%"])
    table.add_row([decor(share_price > sma_50, "Above", "Below") + "  50 SMA", f"{sma_50:.2f}", "$"])
    table.add_row([decor(share_price > sma_100, "Above", "Below") + " 100 SMA", f"{sma_100:.2f}", "$"])
    table.add_row([decor(share_price > sma_150, "Above", "Below") + " 150 SMA", f"{sma_200:.2f}", "$"])
    table.add_row([decor(share_price > sma_200, "Above", "Below") + " 200 SMA", f"{sma_200:.2f}", "$"])
    table.align["Metric"] = "l"
    table.align["Value"] = "r"
    print(table)

    return table


def get(dataframe, key, index=0):
    try:
        value = dataframe.loc[key].iloc[index]
        if pd.isna(value):
            print(f"'{key}' at index {index} is NaN in the DataFrame. Setting value to 0.")
            return 0
        return value
    except KeyError:
        print(f"'{key}' not found in the DataFrame. Setting value to 0.")
        return 0


def decor(condition, true_text, false_text=None):
    if false_text is None:
        false_text = true_text
    if condition:
        return Fore.RED + Style.BRIGHT + true_text + Style.RESET_ALL
    else:
        return Fore.GREEN + Style.BRIGHT + false_text + Style.RESET_ALL
