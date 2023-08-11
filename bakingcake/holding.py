from iexfinance.stocks import Stock
from marshmallow import Schema, fields, post_load, validates, ValidationError
from . import utils


class HoldingSchema(Schema):
    """
        Schema for specifying the holding characteristics.
    """
    account = fields.String(required=True)
    ticker = fields.String(required=True)
    quantity = fields.Float(required=True)
    asset_type = fields.String(required=True)
    apr = fields.Float()
    apy = fields.Float()

    @post_load
    def create_holding(self, input_data, **kwargs):
        return Holding(**input_data)

    @validates("asset_type")
    def validate_quantity(self, asset_type):
        asset_types = ("crypto", "equity", "cash")
        if asset_type not in asset_types:
            raise ValidationError(
                "Invalid asset type provided, please select one of the"
                " following: {}.".format(", ".join(asset_types)))


class Holding(object):
    """
        This class will function as the base object class for a portfolio.
    """

    def __init__(
            self, account, ticker, quantity, asset_type, apr=None, apy=None):
        """
            Holding constructor.
        """
        # Setup required args
        self.account = account
        self.ticker = ticker
        self.quantity = quantity
        # Setup annual percentage rate and yield
        if apr and not apy:
            apy = utils.calculate_apy(apr)
        elif apy and not apr:
            apr = utils.calculate_apr(apy)
        else:
            apr = 0.0
            apy = 0.0
        self.apr = apr
        self.apy = apy
        # TODO: Add list of different base currencies
        self.base_currency = "usd"
        # Get price provided asset type
        self.asset_type = asset_type
        if asset_type == "crypto":
            # Get holding info
            token_info, success = utils.get_token_info(ticker)
            self.id = token_info["id"]
            # Calculate price
            self.price = utils.CG_API.get_price(
                ids=self.id, vs_currencies=self.base_currency
            )[self.id][self.base_currency]
        elif asset_type == "equity":
            self.stock = Stock(ticker)
            self.quote = self.stock.get_quote()
            self.id = self.quote["companyName"][0]
            self.price = self.quote["latestPrice"][0]
        elif asset_type == "cash":
            self.id = "USD"
            self.price = 1.0
        # Calculate the holding total
        self.total = self.price * self.quantity
        # Calculate the annual yield
        self.annual_yield_usd = self.total * self.apy
        self.annual_yield_token = self.quantity * self.apy

        return


def load_holdings(holdings_list):
    """
    This method will load the users holdings based on an input filepath.

    Args:
        holdings_list (list): list of holdings information

    Returns:
        list of holdings objects
    """
    return [HoldingSchema().load(h) for h in holdings_list]
