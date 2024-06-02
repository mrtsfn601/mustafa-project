import numpy as np
import pandas as pd


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


def get_discount_rate(ticker, risk_free_rate=0.02, market_return=0.08):
    """
    Calculate the discount rate using the CAPM (Capital Asset Pricing Model).
    :param ticker: yfinance.Ticker object
    :param risk_free_rate: The risk-free rate of return
    :param market_return: The expected market return
    :return: The discount rate
    """
    beta = ticker.info['beta']
    capm = risk_free_rate + beta * (market_return - risk_free_rate)
    return capm


def get_growth_rate(ticker, years=20):
    """
    Calculate the Compound Annual Growth Rate (CAGR) of the cash flow over a given number of years.
    :param ticker: yfinance.Ticker object
    :param years: The number of years to calculate the growth rate over
    :return: The growth rate of the cash flow
    """
    cash_flow = ticker.cashflow.loc['Total Cash From Operating Activities']
    if len(cash_flow) < years:
        raise ValueError(f"Not enough data to calculate the growth rate over {years} years")
    beginning_value = cash_flow.iloc[-years]
    ending_value = cash_flow.iloc[0]
    cagr = (ending_value / beginning_value) ** (1 / years) - 1
    return cagr


def intrinsic_value_peg_ratio(ticker, years=20):
    """
    Calculate the intrinsic value of a business entity using the PEG ratio (Price/Earnings to Growth ratio).
    :param ticker: yfinance.Ticker object
    :param years: The number of years to calculate the intrinsic value over
    :return: The intrinsic value of the business entity
    """
    peg_ratio = ticker.info['pegRatio']
    growth_rate = get_growth_rate(ticker, years)
    intrinsic_value = peg_ratio * growth_rate
    return intrinsic_value


def get_intrinsic_value(ticker, years=20):
    """
    Calculate the intrinsic value of a business entity using the Discounted Cash Flow (DCF) method.
    :param ticker: yfinance.Ticker object
    :param years: The number of years to calculate the intrinsic value over
    :return: The intrinsic value of the business entity
    """
    cash_flow = ticker.cashflow.loc['Total Cash From Operating Activities'].iloc[0]
    growth_rate = get_growth_rate(ticker, years)
    discount_rate = get_discount_rate(ticker)
    dcf = sum([cash_flow * (1 + growth_rate) ** year / (1 + discount_rate) ** year for year in range(1, years + 1)])
    shares_outstanding = ticker.info['sharesOutstanding']
    intrinsic_value = dcf / shares_outstanding
    return intrinsic_value
