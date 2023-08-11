import os
import yaml
from marshmallow import Schema, fields, post_load, validates, ValidationError
import pandas as pd
from . import holding


class PortfolioSchema(Schema):
    """
        Schema for specifying the holding characteristics.
    """
    holdings = fields.List(
        fields.Nested(holding.HoldingSchema), required=True)

    @post_load
    def create_portfolio(self, input_data, **kwargs):
        return Portfolio(**input_data)


class Portfolio(object):
    """
        This class will function as the base object class for a portfolio.
    """

    def __init__(self, holdings):
        """
            Portfolio constructor.
        """
        self.holdings = holdings
        # Calculate sums per asset
        self.assets_df, self.portfolio_total = get_asset_df_and_total(
            self.holdings)
        # Get portfolio metrics
        self.portfolio_yeild = calculate_portfolio_yield(self.holdings)

        # TODO: Add sums per asset class

        # TODO: Add USD

        # TODO: Add assets earning interest

        return


# --- Portfolio specific functions ---
def load_portfolio(input_path):
    """
        Load portfolio object provided a file path.

        Args:
            input_path (str): portfolio file input path

        Returns:
            portfolio object
    """
    # Pull file extension
    filename, extension = os.path.splitext(input_path)
    # Parse YAML portfolio file
    if extension in (".yaml", "yml"):
        portfolio_args = yaml.safe_load(open(input_path, "r"))
    elif extension == ".csv":
        portfolio_args = {
            "holdings": pd.read_csv(input_path).to_dict("records")}
    else:
        # TODO: Add error handling here
        pass


    return PortfolioSchema().load(portfolio_args)


def get_asset_df_and_total(holdings):
    """
        Add sums per asset and return asset dict.

        TODO: Switch to asset pandas DataFrame

        Args:
            holdings (list): list of portfolio holdings

        Returns:
            asset dict
    """
    assets = {}
    for h in holdings:
        asset_str = h.asset_type + "-" + h.ticker
        if asset_str not in assets:
            assets[asset_str] = {
                "asset_type": h.asset_type,
                "ticker": h.ticker,
                "quantity": h.quantity,
                "price": h.price,
                "total": h.total,
                "annual_yield_usd": h.annual_yield_usd}
        else:
            assets[asset_str]["quantity"] += h.quantity
            assets[asset_str]["price"] += h.price
            assets[asset_str]["total"] += h.total
            assets[asset_str]["annual_yield_usd"] += h.annual_yield_usd
    # Cast dict to DataFrame
    assets_df = pd.DataFrame(assets).T.reset_index()
    # Calculate total
    total = assets_df.total.sum()
    # Calculate percentages
    assets_df["allocation_percentage"] = assets_df.total / total
    # Sort by allocation percentage and reset index
    assets_df = assets_df.sort_values(
        by="allocation_percentage", ascending=False).reset_index(drop=True)

    return assets_df, total


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
