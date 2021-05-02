"""
This module will house the interest calculation engine of baking cake.
"""
import yaml
import pandas as pd
from pycoingecko import CoinGeckoAPI

# Initialize
CG_API = CoinGeckoAPI()
# Get the coin list
COIN_LIST = CG_API.get_coins_list()


def load_holdings(input_path):
    """
    This method will load the users holdings based on an input filepath.

    Args:
        input_path (str): path to users holdings file

    Returns:
        analysis of holdings
    """
    holdings = yaml.safe_load(open("bakingcake/holdings/tokens.yaml", "r"))
    # Iterate over holdings and get id and prices
    for i in range(len(holdings["holdings"])):
        token_info, success = get_token_info(holdings["holdings"][i]["ticker"])
        holdings["holdings"][i]["id"] = token_info["id"]
        holdings["holdings"][i]["price"] = CG_API.get_price(
            ids=holdings["holdings"][i]["id"], vs_currencies='usd'
        )[holdings["holdings"][i]["id"]]["usd"]
        # Calculate the total holdings in USD
        holdings["holdings"][i]["total"] = (
            holdings["holdings"][i]["price"] *
            holdings["holdings"][i]["quantity"])
        # Calculate the 1 year yield
        holdings["holdings"][i]["1_year_yield_usd"] = (
            holdings["holdings"][i]["total"] *
            (holdings["holdings"][i]["apy"] / 100.0))
        holdings["holdings"][i]["1_year_yield_token"] = (
            holdings["holdings"][i]["quantity"] *
            (holdings["holdings"][i]["apy"] / 100.0))

    return holdings


def calculate_portfolio_yield(holdings):
    """
        This method will calculate the overall yield of the portfolio.

        Args:
            holdings (dict): portfolio holdings

        Returns:
            portfolio yield
    """
    portfolio_yield = {}
    portfolio_yield["one_year_yield"] = sum(
        [i["1_year_yield_usd"] for i in holdings["holdings"]])
    portfolio_yield["one_day_yield"] = (
        portfolio_yield["one_year_yield"] / 365.0)

    return portfolio_yield


def get_token_info(ticker):
    """
    Get the information provided a token's ticker.

    Args:
        ticker (str): ticker symbol as a string

    Return:
        ticker information
    """
    success = False
    token_info = {}
    token_list = [i for i in COIN_LIST if ticker.lower() == i["symbol"]]
    if token_list:
        success = True
        if len(token_list) == 1:
            token_info = token_list[0]
        else:
            i = 0
            while True:
                token_info = token_list[i]
                if (
                    "governance" not in token_info["id"] and
                    "-" in token_info["id"]
                ):
                    i += 1
                else:
                    break

    return token_info, success
