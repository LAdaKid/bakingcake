"""
This module will house the interest calculation engine of baking cake.
"""
import yaml
import numpy as np
import pandas as pd
from . import holdings


def load_holdings(input_path):
    """
    This method will load the users holdings based on an input filepath.

    Args:
        input_path (str): path to users holdings file

    Returns:
        analysis of holdings
    """
    holdings_list = []
    holdings_dict = yaml.safe_load(open(input_path, "r"))
    # Iterate over holdings and get id and prices
    #for i in range(len(holdings_dict["holdings"])):
    for holding in holdings_dict["holdings"]:
        holdings_list.append(
            holdings.HoldingSchema().load(holding))

    return holdings_list


def calculate_portfolio_yield(holdings_list):
    """
        This method will calculate the overall yield of the portfolio.

        Args:
            holdings_list (list): list of portfolio holdings

        Returns:
            portfolio yield
    """
    portfolio_yield = {}
    portfolio_yield["one_year_yield"] = sum(
        [h.annual_yield_usd for h in holdings_list])
    portfolio_yield["one_day_yield"] = (
        portfolio_yield["one_year_yield"] / 365.0)

    return portfolio_yield
